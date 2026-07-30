#!/usr/bin/env python3
"""
ZAOU-GenDoc — Interface Web Locale
Tableau de bord officiel du Secrétariat du Sénat pour la génération
automatique des relevés de notes ZAOU.
"""

import json
import os
import sys
import hashlib
import time
import threading
import webbrowser
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import io
import base64

BASE_DIR = Path(__file__).resolve().parent

# Ajouter le dossier scripts au path
sys.path.insert(0, str(BASE_DIR / 'scripts'))
from validate_data import validate_student_record, GRADE_POINTS
from generate_qr import generate_verification_qr_data_uri
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML


def load_students():
    data_file = BASE_DIR / 'data' / 'test_senate_bit_2012_2017.json'
    with open(data_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_single_pdf(student):
    """Génère un seul PDF pour un étudiant et retourne son chemin + hash."""
    output_dir = BASE_DIR / 'output' / 'pdfs'
    os.makedirs(output_dir, exist_ok=True)

    validate_student_record(student)

    student_id = student['student_id']
    safe_id = student_id.replace('/', '_')

    initial_hash = hashlib.sha256(
        f"{student_id}_{student['full_name']}_{student['gpa']}".encode()
    ).hexdigest()

    qr_data_uri = generate_verification_qr_data_uri(student_id, initial_hash)

    logo_path = (BASE_DIR / 'assets' / 'zaou_logo.png').as_uri()
    seal_path = (BASE_DIR / 'assets' / 'university_seal.png').as_uri()
    sig_path  = (BASE_DIR / 'assets' / 'registrar_signature.png').as_uri()

    env = Environment(loader=FileSystemLoader(str(BASE_DIR / 'templates')))
    template = env.get_template('transcript_2012_2017.html')
    html_content = template.render(
        student=student,
        logo_path=logo_path,
        seal_path=seal_path,
        sig_path=sig_path,
        qr_data_uri=qr_data_uri,
        sha256_short=initial_hash[:16].upper()
    )

    pdf_filename = f"{safe_id}_BIT_TRANSCRIPT.pdf"
    pdf_path = output_dir / pdf_filename

    pdf_bytes = HTML(string=html_content, base_url=str(BASE_DIR / 'templates')).write_pdf()
    final_hash = hashlib.sha256(pdf_bytes).hexdigest()

    with open(pdf_path, 'wb') as f:
        f.write(pdf_bytes)

    # Mise à jour du journal d'audit
    audit_file = BASE_DIR / 'output' / 'audit_log.json'
    audit = []
    if audit_file.exists():
        with open(audit_file) as f:
            audit = json.load(f)

    audit = [e for e in audit if e.get('student_id') != student_id]
    audit.append({
        'student_id': student_id,
        'full_name': student['full_name'],
        'programme': student['programme'],
        'gpa': student.get('calculated_gpa', student.get('gpa', 0)),
        'qualification_class': student.get('calculated_class', student.get('qualification_class', '')),
        'pdf_filename': pdf_filename,
        'sha256_hash': final_hash,
        'issued_at': time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime()),
        'authority': 'Office of the Senate Secretariat - Zambian Open University'
    })

    with open(audit_file, 'w', encoding='utf-8') as f:
        json.dump(audit, f, indent=2, ensure_ascii=False)

    return str(pdf_path), final_hash


HTML_PAGE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>ZAOU-GenDoc — Secrétariat du Sénat</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap');

  :root {
    --green: #006633;
    --green-light: #00994d;
    --gold: #c8a000;
    --gold-light: #ffcc00;
    --dark: #0a1628;
    --card: #111d35;
    --border: #1e3150;
    --text: #e8eaf0;
    --muted: #8899bb;
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    font-family: 'Outfit', sans-serif;
    background: var(--dark);
    color: var(--text);
    min-height: 100vh;
  }

  /* HEADER */
  .header {
    background: linear-gradient(135deg, #012a14 0%, #003d1f 50%, #011a40 100%);
    border-bottom: 2px solid var(--gold);
    padding: 18px 40px;
    display: flex;
    align-items: center;
    gap: 20px;
    box-shadow: 0 4px 30px rgba(0,0,0,0.4);
  }
  .header-logo {
    width: 60px; height: 60px;
    border-radius: 50%;
    border: 2px solid var(--gold);
    object-fit: cover;
  }
  .header-text h1 {
    font-size: 1.2rem; font-weight: 800;
    color: var(--gold-light);
    letter-spacing: 1px;
    text-transform: uppercase;
  }
  .header-text p {
    font-size: 0.78rem; color: var(--muted);
    text-transform: uppercase; letter-spacing: 0.5px;
  }
  .header-badge {
    margin-left: auto;
    background: rgba(198,160,0,0.15);
    border: 1px solid var(--gold);
    color: var(--gold-light);
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 0.75rem; font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  /* MAIN LAYOUT */
  .container {
    max-width: 1100px;
    margin: 0 auto;
    padding: 36px 24px;
  }

  /* STAT CARDS */
  .stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin-bottom: 36px;
  }
  .stat-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px;
    text-align: center;
    transition: transform 0.2s;
  }
  .stat-card:hover { transform: translateY(-3px); }
  .stat-card .number {
    font-size: 2.5rem; font-weight: 800;
    background: linear-gradient(135deg, var(--green-light), var(--gold-light));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  .stat-card .label {
    font-size: 0.78rem; color: var(--muted);
    text-transform: uppercase; letter-spacing: 1px;
    margin-top: 4px;
  }

  /* MAIN CARD */
  .main-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 18px;
    overflow: hidden;
    margin-bottom: 28px;
  }
  .card-header {
    padding: 20px 28px;
    background: linear-gradient(90deg, rgba(0,102,51,0.3), rgba(0,0,0,0));
    border-bottom: 1px solid var(--border);
    font-size: 1rem; font-weight: 700;
    color: var(--gold-light);
    text-transform: uppercase;
    letter-spacing: 1px;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .card-header span { font-size: 1.3rem; }

  /* SEARCH & FORM */
  .search-form {
    padding: 24px 28px;
    border-bottom: 1px solid var(--border);
    display: flex; gap: 12px; flex-wrap: wrap; align-items: center;
  }
  .search-form input, .search-form select {
    background: #0d1e38;
    border: 1px solid var(--border);
    color: var(--text);
    padding: 10px 16px;
    border-radius: 10px;
    font-size: 0.9rem;
    font-family: 'Outfit', sans-serif;
    flex: 1; min-width: 160px;
  }
  .search-form input:focus, .search-form select:focus {
    outline: none;
    border-color: var(--green-light);
  }
  .btn {
    padding: 10px 24px;
    border: none; border-radius: 10px;
    font-size: 0.9rem; font-weight: 700;
    cursor: pointer; transition: all 0.2s;
    font-family: 'Outfit', sans-serif;
    text-transform: uppercase; letter-spacing: 0.5px;
    text-decoration: none; display: inline-block;
  }
  .btn-green { background: var(--green); color: white; }
  .btn-green:hover { background: var(--green-light); transform: translateY(-1px); }
  .btn-gold { background: var(--gold); color: #000; }
  .btn-gold:hover { background: var(--gold-light); transform: translateY(-1px); }
  .btn-sm { padding: 7px 16px; font-size: 0.8rem; }

  /* TABLE */
  .table-wrap { overflow-x: auto; }
  table { width: 100%; border-collapse: collapse; }
  thead tr { background: rgba(0,102,51,0.2); }
  th {
    padding: 12px 16px;
    font-size: 0.75rem; font-weight: 700;
    color: var(--gold-light); text-transform: uppercase; letter-spacing: 1px;
    text-align: left; border-bottom: 1px solid var(--border);
  }
  td {
    padding: 13px 16px;
    font-size: 0.88rem;
    border-bottom: 1px solid rgba(30,49,80,0.5);
    vertical-align: middle;
  }
  tr:hover td { background: rgba(255,255,255,0.02); }
  .badge {
    padding: 3px 12px; border-radius: 20px;
    font-size: 0.72rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .badge-distinction { background: rgba(0,153,77,0.2); color: #00e676; border: 1px solid #00994d; }
  .badge-merit       { background: rgba(30,120,255,0.2); color: #7eb5ff; border: 1px solid #1e78ff; }
  .badge-credit      { background: rgba(200,160,0,0.2); color: #ffd740; border: 1px solid #c8a000; }
  .badge-satisfactory{ background: rgba(150,80,0,0.2); color: #ffab40; border: 1px solid #964f00; }

  /* TOAST */
  #toast {
    position: fixed; bottom: 30px; right: 30px;
    background: var(--green); color: white;
    padding: 14px 24px; border-radius: 12px;
    font-weight: 700; font-size: 0.9rem;
    box-shadow: 0 8px 30px rgba(0,0,0,0.4);
    display: none; z-index: 999;
    animation: slideUp 0.3s ease;
  }
  @keyframes slideUp {
    from { transform: translateY(20px); opacity: 0; }
    to   { transform: translateY(0);    opacity: 1; }
  }

  /* SPINNER */
  .spinner {
    display: inline-block; width: 16px; height: 16px;
    border: 2px solid rgba(255,255,255,0.3);
    border-top-color: white;
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
    vertical-align: middle; margin-right: 6px;
  }
  @keyframes spin { to { transform: rotate(360deg); } }

  .no-students { padding: 40px; text-align: center; color: var(--muted); font-size: 0.9rem; }
  .id-mono { font-family: monospace; font-size: 0.82rem; color: var(--muted); }
</style>
</head>
<body>

<div class="header">
  <img class="header-logo" src="/logo" alt="ZAOU">
  <div class="header-text">
    <h1>ZAOU-GenDoc</h1>
    <p>Secrétariat du Sénat — Bureau du Registre Adjoint (Academic Affairs)</p>
  </div>
  <div class="header-badge">✦ Système Actif</div>
</div>

<div class="container">
  <!-- Stats -->
  <div class="stats">
    <div class="stat-card">
      <div class="number" id="stat-total">—</div>
      <div class="label">Étudiants dans le registre</div>
    </div>
    <div class="stat-card">
      <div class="number" id="stat-pdfs">—</div>
      <div class="label">Relevés générés</div>
    </div>
    <div class="stat-card">
      <div class="number" id="stat-distinction">—</div>
      <div class="label">Distinctions</div>
    </div>
    <div class="stat-card">
      <div class="number" id="stat-speed">0.65s</div>
      <div class="label">Vitesse / document</div>
    </div>
  </div>

  <!-- Tableau Principal -->
  <div class="main-card">
    <div class="card-header">
      <span>📋</span> Registre de Délibération du Sénat — BIT 2012–2017
    </div>
    <div class="search-form">
      <input type="text" id="searchInput" placeholder="🔍  Rechercher un étudiant (nom ou matricule)..." oninput="filterTable()">
      <select id="filterClass" onchange="filterTable()">
        <option value="">— Toutes les mentions —</option>
        <option value="DISTINCTION">Distinction</option>
        <option value="MERIT">Merit</option>
        <option value="CREDIT">Credit</option>
        <option value="SATISFACTORY">Satisfactory</option>
      </select>
      <button class="btn btn-green" onclick="generateAllPdfs()">⬇ Générer TOUS les PDFs</button>
    </div>
    <div class="table-wrap">
      <table id="studentTable">
        <thead>
          <tr>
            <th>#</th>
            <th>Nom Complet</th>
            <th>Matricule</th>
            <th>Session</th>
            <th>GPA</th>
            <th>Mention</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody id="tableBody">
          <tr><td colspan="7" class="no-students">Chargement du registre…</td></tr>
        </tbody>
      </table>
    </div>
  </div>

</div>

<div id="toast"></div>

<script>
let students = [];

function classColor(cls) {
  if (!cls) return '';
  const m = cls.toLowerCase();
  if (m === 'distinction') return 'badge-distinction';
  if (m === 'merit') return 'badge-merit';
  if (m === 'credit') return 'badge-credit';
  return 'badge-satisfactory';
}

async function loadStudents() {
  const res = await fetch('/api/students');
  const data = await res.json();
  students = data.students;

  document.getElementById('stat-total').textContent = students.length;
  document.getElementById('stat-distinction').textContent = students.filter(s => s.qualification_class === 'DISTINCTION').length;

  await countPdfs();
  renderTable(students);
}

async function countPdfs() {
  const res = await fetch('/api/pdfs/count');
  const d = await res.json();
  document.getElementById('stat-pdfs').textContent = d.count;
}

function renderTable(list) {
  const tbody = document.getElementById('tableBody');
  if (!list.length) {
    tbody.innerHTML = '<tr><td colspan="7" class="no-students">Aucun étudiant trouvé.</td></tr>';
    return;
  }
  tbody.innerHTML = list.map((s, i) => `
    <tr>
      <td style="color:var(--muted)">${i+1}</td>
      <td><strong>${s.full_name}</strong></td>
      <td class="id-mono">${s.student_id}</td>
      <td>${s.graduation_session}</td>
      <td><strong style="color:var(--gold-light)">${s.gpa}</strong></td>
      <td><span class="badge ${classColor(s.qualification_class)}">${s.qualification_class}</span></td>
      <td>
        <button class="btn btn-gold btn-sm" onclick="generatePdf('${s.student_id}', this)">
          ⬇ Générer
        </button>
      </td>
    </tr>
  `).join('');
}

function filterTable() {
  const q = document.getElementById('searchInput').value.toLowerCase();
  const cls = document.getElementById('filterClass').value;
  const filtered = students.filter(s => {
    const matchQ = !q || s.full_name.toLowerCase().includes(q) || s.student_id.toLowerCase().includes(q);
    const matchC = !cls || s.qualification_class === cls;
    return matchQ && matchC;
  });
  renderTable(filtered);
}

function showToast(msg, color='var(--green)') {
  const t = document.getElementById('toast');
  t.style.background = color;
  t.innerHTML = msg;
  t.style.display = 'block';
  setTimeout(() => { t.style.display = 'none'; }, 4000);
}

async function generatePdf(studentId, btn) {
  const orig = btn.innerHTML;
  btn.innerHTML = '<span class="spinner"></span>Génération…';
  btn.disabled = true;

  try {
    const res = await fetch('/api/generate', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({student_id: studentId})
    });
    const d = await res.json();
    if (d.success) {
      showToast(`✅ Relevé généré : ${d.filename}`);
      await countPdfs();
      // Auto-open PDF
      window.open('/download/' + encodeURIComponent(d.filename), '_blank');
    } else {
      showToast(`❌ Erreur : ${d.error}`, '#cc2200');
    }
  } catch(e) {
    showToast('❌ Erreur réseau', '#cc2200');
  }

  btn.innerHTML = orig;
  btn.disabled = false;
}

async function generateAllPdfs() {
  showToast('⏳ Génération de tous les relevés en cours…', '#004488');
  const res = await fetch('/api/generate_all', {method: 'POST'});
  const d = await res.json();
  if (d.success) {
    showToast(`✅ ${d.count} relevés générés en ${d.elapsed}s`);
    await countPdfs();
  } else {
    showToast('❌ Erreur lors de la génération', '#cc2200');
  }
}

loadStudents();
</script>
</body>
</html>
"""


class ZAOUHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Silence les logs du serveur

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == '/' or path == '/index.html':
            body = HTML_PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', len(body))
            self.end_headers()
            self.wfile.write(body)

        elif path == '/logo':
            logo_path = BASE_DIR / 'assets' / 'zaou_logo.png'
            with open(logo_path, 'rb') as f:
                data = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'image/png')
            self.send_header('Content-Length', len(data))
            self.end_headers()
            self.wfile.write(data)

        elif path == '/api/students':
            dataset = load_students()
            self.send_json(dataset)

        elif path == '/api/pdfs/count':
            pdf_dir = BASE_DIR / 'output' / 'pdfs'
            count = len(list(pdf_dir.glob('*.pdf'))) if pdf_dir.exists() else 0
            self.send_json({'count': count})

        elif path.startswith('/download/'):
            filename = path[len('/download/'):]
            pdf_path = BASE_DIR / 'output' / 'pdfs' / filename
            if pdf_path.exists():
                with open(pdf_path, 'rb') as f:
                    data = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/pdf')
                self.send_header('Content-Disposition', f'inline; filename="{filename}"')
                self.send_header('Content-Length', len(data))
                self.end_headers()
                self.wfile.write(data)
            else:
                self.send_json({'error': 'Fichier introuvable'}, 404)

        else:
            self.send_json({'error': 'Route non trouvée'}, 404)

    def do_POST(self):
        path = urlparse(self.path).path
        length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(length)) if length else {}

        if path == '/api/generate':
            student_id = body.get('student_id', '')
            dataset = load_students()
            student = next((s for s in dataset['students'] if s['student_id'] == student_id), None)
            if not student:
                self.send_json({'success': False, 'error': 'Étudiant non trouvé'}, 404)
                return
            try:
                t0 = time.time()
                pdf_path, sha256 = generate_single_pdf(student)
                elapsed = round(time.time() - t0, 2)
                self.send_json({
                    'success': True,
                    'filename': Path(pdf_path).name,
                    'sha256': sha256,
                    'elapsed': elapsed
                })
            except Exception as e:
                self.send_json({'success': False, 'error': str(e)}, 500)

        elif path == '/api/generate_all':
            dataset = load_students()
            students = dataset['students']
            env = Environment(loader=FileSystemLoader(str(BASE_DIR / 'templates')))
            t0 = time.time()
            count = 0
            output_dir = BASE_DIR / 'output' / 'pdfs'
            os.makedirs(output_dir, exist_ok=True)
            audit_records = []
            for student in students:
                try:
                    pdf_path, sha256 = generate_single_pdf(student)
                    count += 1
                except Exception:
                    pass
            elapsed = round(time.time() - t0, 2)
            self.send_json({'success': True, 'count': count, 'elapsed': elapsed})

        else:
            self.send_json({'error': 'Route non trouvée'}, 404)


def run_server(port=8765):
    server = HTTPServer(('localhost', port), ZAOUHandler)
    print(f"\n{'='*60}")
    print(f"  ZAOU-GenDoc — Interface Web Opérationnelle")
    print(f"  Secrétariat du Sénat — Zambian Open University")
    print(f"{'='*60}")
    print(f"\n  ➤ Accès : http://localhost:{port}")
    print(f"  ➤ Appuyez sur Ctrl+C pour arrêter le serveur\n")
    threading.Timer(1.2, lambda: webbrowser.open(f'http://localhost:{port}')).start()
    server.serve_forever()


if __name__ == '__main__':
    run_server()
