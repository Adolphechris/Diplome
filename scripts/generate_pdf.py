import os
import sys
import json
import time
import hashlib
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

from validate_data import validate_student_record
from generate_qr import generate_verification_qr_data_uri

BASE_DIR = Path(__file__).resolve().parent.parent

def build_pdf_for_student(student, env, output_dir, audit_records, etranscript=False):
    """
    Renders HTML transcript template with student data, compiles PDF via WeasyPrint,
    computes binary SHA-256 hash, and logs transaction into audit_log.json.
    
    Args:
        etranscript: If True, generates the Electronic (E-Transcript) version with
                     background watermark and green security badge.
    """
    student_id = student["student_id"]
    safe_id    = student_id.replace("/", "_")
    
    # 1. Validation & GPA recalculation
    validate_student_record(student)
    
    # 2. Pre-hash placeholder for QR Code encoding
    initial_hash = hashlib.sha256(
        f"{student_id}_{student['full_name']}_{student['gpa']}".encode('utf-8')
    ).hexdigest()
    
    # 3. Dynamic QR Code Data URI
    qr_data_uri = generate_verification_qr_data_uri(student_id, initial_hash)
    
    # Absolute paths for template images
    logo_path = (BASE_DIR / "assets" / "zaou_logo.png").as_uri()
    seal_path = (BASE_DIR / "assets" / "university_seal.png").as_uri()
    sig_path  = (BASE_DIR / "assets" / "registrar_signature.png").as_uri()
    
    # 4. Render HTML Template (version normale OU e-transcript)
    template = env.get_template("transcript_2012_2017.html")
    html_content = template.render(
        student=student,
        logo_path=logo_path,
        seal_path=seal_path,
        sig_path=sig_path,
        qr_data_uri=qr_data_uri,
        sha256_short=initial_hash[:16].upper(),
        is_etranscript=etranscript
    )
    
    # 5. Nom du fichier selon la version
    if etranscript:
        pdf_filename = f"{safe_id}_BIT_E-TRANSCRIPT.pdf"
    else:
        pdf_filename = f"{safe_id}_BIT_TRANSCRIPT.pdf"
    
    pdf_path = output_dir / pdf_filename
    
    # 6. WeasyPrint PDF Compilation
    html_obj  = HTML(string=html_content, base_url=str(BASE_DIR / "templates"))
    pdf_bytes = html_obj.write_pdf()
    
    # 7. Compute Final SHA-256 Binary Hash
    final_sha256 = hashlib.sha256(pdf_bytes).hexdigest()
    
    # Write PDF to disk
    with open(pdf_path, 'wb') as f:
        f.write(pdf_bytes)
    
    # 8. Add Audit Trail Entry
    doc_type = "E-TRANSCRIPT" if etranscript else "TRANSCRIPT"
    audit_entry = {
        "student_id":         student_id,
        "full_name":          student["full_name"],
        "programme":          student["programme"],
        "document_type":      doc_type,
        "gpa":                student.get("calculated_gpa", student.get("gpa", 0)),
        "qualification_class":student.get("calculated_class", student.get("qualification_class", "")),
        "pdf_filename":       pdf_filename,
        "sha256_hash":        final_sha256,
        "issued_at":          time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "authority":          "Office of the Senate Secretariat - Zambian Open University"
    }
    audit_records.append(audit_entry)
    
    return pdf_path, final_sha256


def main():
    """
    Génère DEUX versions pour chaque étudiant :
      1. VERSION IMPRIMÉE  → output/pdfs/     (*_TRANSCRIPT.pdf)
      2. VERSION ÉLECTRONIQUE → output/etranscripts/  (*_E-TRANSCRIPT.pdf)
         avec filigrane ZAOU visible en arrière-plan et badge sécurisé vert.
    """
    start_time = time.time()
    
    # Répertoires
    data_file      = BASE_DIR / "data" / "test_senate_bit_2012_2017.json"
    templates_dir  = BASE_DIR / "templates"
    pdf_dir        = BASE_DIR / "output" / "pdfs"
    etrans_dir     = BASE_DIR / "output" / "etranscripts"
    audit_log_file = BASE_DIR / "output" / "audit_log.json"
    
    os.makedirs(pdf_dir,        exist_ok=True)
    os.makedirs(etrans_dir,     exist_ok=True)
    os.makedirs(audit_log_file.parent, exist_ok=True)
    
    # Jinja2 Environment
    env = Environment(loader=FileSystemLoader(str(templates_dir)))
    
    # Chargement du registre de délibération du Sénat
    with open(data_file, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    
    students = dataset.get("students", [])
    total    = len(students)
    print(f"\n{'='*65}")
    print(f"ZAOU-GenDoc — Double Generation Engine")
    print(f"  {total} students → VERSION IMPRIMÉE + VERSION ÉLECTRONIQUE")
    print(f"{'='*65}\n")
    
    audit_records = []
    
    for idx, student in enumerate(students, 1):
        # --- Version Imprimée (classique, sans filigrane) ---
        pdf_path, sha256 = build_pdf_for_student(
            student, env, pdf_dir, audit_records, etranscript=False
        )
        
        # --- Version Électronique (avec filigrane + badge) ---
        etr_path, esha256 = build_pdf_for_student(
            student, env, etrans_dir, audit_records, etranscript=True
        )
        
        if idx <= 3 or idx % 10 == 0:
            print(f"[{idx:2d}/{total}] PRINTED  : {pdf_path.name} | SHA256: {sha256[:16]}..")
            print(f"         E-TRANS : {etr_path.name} | SHA256: {esha256[:16]}..")
            print()
    
    # Registre d'audit central
    with open(audit_log_file, 'w', encoding='utf-8') as f:
        json.dump(audit_records, f, indent=2, ensure_ascii=False)
    
    elapsed     = time.time() - start_time
    avg_per_doc = elapsed / (total * 2) if total else 0
    
    print("="*65)
    print(f"✅ SUCCESS: {total * 2} PDFs générés en {elapsed:.2f} secondes.")
    print(f"   · {total} Relevés Imprimés  → {pdf_dir}")
    print(f"   · {total} E-Transcripts     → {etrans_dir}")
    print(f"   Vitesse moyenne : {avg_per_doc:.3f}s / document (Cible < 2.0s)")
    print(f"   Journal d'Audit : {audit_log_file}")
    print("="*65 + "\n")


if __name__ == '__main__':
    main()
