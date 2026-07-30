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

def build_pdf_for_student(student, env, output_dir, audit_records):
    """
    Renders HTML transcript template with student data, compiles PDF via WeasyPrint,
    computes binary SHA-256 hash, and logs transaction into audit_log.json.
    """
    student_id = student["student_id"]
    safe_id = student_id.replace("/", "_")
    
    # 1. Validation & GPA recalculation
    validate_student_record(student)
    
    # 2. Pre-hash placeholder for QR Code encoding
    initial_hash = hashlib.sha256(f"{student_id}_{student['full_name']}_{student['gpa']}".encode('utf-8')).hexdigest()
    
    # 3. Dynamic QR Code Data URI
    qr_data_uri = generate_verification_qr_data_uri(student_id, initial_hash)
    
    # Absolute paths for template images
    logo_path = (BASE_DIR / "assets" / "zaou_logo.png").as_uri()
    seal_path = (BASE_DIR / "assets" / "university_seal.png").as_uri()
    sig_path = (BASE_DIR / "assets" / "registrar_signature.png").as_uri()
    
    # 4. Render HTML Template
    template = env.get_template("transcript_2012_2017.html")
    html_content = template.render(
        student=student,
        logo_path=logo_path,
        seal_path=seal_path,
        sig_path=sig_path,
        qr_data_uri=qr_data_uri,
        sha256_short=initial_hash[:16].upper()
    )
    
    # 5. WeasyPrint PDF Compilation
    pdf_filename = f"{safe_id}_BIT_TRANSCRIPT.pdf"
    pdf_path = output_dir / pdf_filename
    
    html_obj = HTML(string=html_content, base_url=str(BASE_DIR / "templates"))
    pdf_bytes = html_obj.write_pdf()
    
    # 6. Compute Final SHA-256 Binary Hash
    final_sha256 = hashlib.sha256(pdf_bytes).hexdigest()
    
    # Write PDF to disk
    with open(pdf_path, 'wb') as f:
        f.write(pdf_bytes)
        
    # 7. Add Audit Trail Entry
    audit_entry = {
        "student_id": student_id,
        "full_name": student["full_name"],
        "programme": student["programme"],
        "gpa": student["gpa"],
        "qualification_class": student["qualification_class"],
        "pdf_filename": pdf_filename,
        "sha256_hash": final_sha256,
        "issued_at": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "authority": "Office of the Senate Secretariat - Zambian Open University"
    }
    audit_records.append(audit_entry)
    
    return pdf_path, final_sha256

def main():
    start_time = time.time()
    
    # Directories
    data_file = BASE_DIR / "data" / "test_senate_bit_2012_2017.json"
    templates_dir = BASE_DIR / "templates"
    output_pdf_dir = BASE_DIR / "output" / "pdfs"
    audit_log_file = BASE_DIR / "output" / "audit_log.json"
    
    os.makedirs(output_pdf_dir, exist_ok=True)
    os.makedirs(audit_log_file.parent, exist_ok=True)
    
    # Jinja2 Environment
    env = Environment(loader=FileSystemLoader(str(templates_dir)))
    
    # Load Senate Deliberation Data
    with open(data_file, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
        
    students = dataset.get("students", [])
    print(f"Starting ZAOU-GenDoc PDF Engine for {len(students)} student records...")
    
    audit_records = []
    generated_pdfs = []
    
    for idx, student in enumerate(students, 1):
        pdf_path, sha256_hash = build_pdf_for_student(student, env, output_pdf_dir, audit_records)
        generated_pdfs.append(pdf_path)
        if idx <= 3 or idx % 10 == 0:
            print(f"[{idx}/{len(students)}] Generated: {pdf_path.name} | SHA-256: {sha256_hash[:16]}...")
            
    # Write Central Audit Log
    with open(audit_log_file, 'w', encoding='utf-8') as f:
        json.dump(audit_records, f, indent=2, ensure_ascii=False)
        
    elapsed = time.time() - start_time
    avg_per_doc = elapsed / len(students) if students else 0
    
    print("\n" + "="*65)
    print(f"SUCCESS: Generated {len(students)} Official Transcripts in {elapsed:.2f} seconds.")
    print(f"Average Processing Speed: {avg_per_doc:.3f} seconds / document (Target < 2.0s).")
    print(f"PDF Output Directory: {output_pdf_dir}")
    print(f"Audit Trail Saved To: {audit_log_file}")
    print("="*65)

if __name__ == '__main__':
    main()
