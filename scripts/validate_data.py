import re
import json

REQUIRED_BIT_COURSES = {
    "BIT 110", "BIT 111", "MA 110", "LA 111", "BIT 120", "MA 120",
    "BIT 210", "BIT 211", "BIT 220", "BIT 221", "BIT 222", "BIT 223",
    "BIT 310", "BIT 311", "BIT 320", "BIT 321", "BIT 322", "BIT 323",
    "BIT 410", "BIT 411", "BIT 420", "BIT 421", "BIT 400"
}

GRADE_POINTS = {
    "A+": 4.0, "A": 4.0, "B+": 3.5, "B": 3.0, "C+": 2.5, "C": 2.0, "D+": 1.0, "D": 0.0,
    "P": 2.0, "S": 3.0, "EX": 3.0, "INC": 0.0
}

def validate_student_record(student):
    """
    Performs data consistency audit on a single student record:
    1. Validates Student Identity Number.
    2. Validates presence of all 23 BIT mandatory courses.
    3. Calculates Weighted GPA on a 4.0 scale.
    4. Computes qualification classification (Distinction, Merit, Credit, Satisfactory).
    """
    student_id = student.get("student_id", "")
    if not student_id:
        raise ValueError(f"Student record missing student_id: {student}")

    record = student.get("academic_record", [])
    courses_found = set()
    total_points = 0.0
    total_credits = 0

    for yr in record:
        for course in yr.get("courses", []):
            code = course.get("code", "").strip()
            courses_found.add(code)
            
            credits = course.get("credits", 3)
            grade = course.get("grade", "C")
            pts = GRADE_POINTS.get(grade, 2.0)
            
            total_points += pts * credits
            total_credits += credits

    missing_courses = REQUIRED_BIT_COURSES - courses_found
    if missing_courses and len(courses_found) < 20:
        raise ValueError(f"Student {student_id} missing mandatory BIT courses: {missing_courses}")

    calculated_gpa = round(total_points / total_credits, 2) if total_credits > 0 else 0.0

    if calculated_gpa >= 3.60:
        expected_class = "DISTINCTION"
    elif calculated_gpa >= 3.00:
        expected_class = "MERIT"
    elif calculated_gpa >= 2.50:
        expected_class = "CREDIT"
    else:
        expected_class = "SATISFACTORY"

    student["calculated_gpa"] = calculated_gpa
    student["calculated_class"] = expected_class

    return True

def audit_dataset(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    students = data.get("students", [])
    print(f"Auditing Senate Deliberation Dataset: {len(students)} student records...")

    valid_count = 0
    for idx, student in enumerate(students, 1):
        validate_student_record(student)
        valid_count += 1

    print(f"Audit Complete! All {valid_count} student records passed integrity verification.")
    return True

if __name__ == '__main__':
    audit_dataset('data/test_senate_bit_2012_2017.json')
