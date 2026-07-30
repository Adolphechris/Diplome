import json
import os
import random

COURSES_YEAR_1 = [
    {"code": "BIT 110", "title": "Introduction to Information Technology", "credits": 3},
    {"code": "BIT 111", "title": "Fundamentals of Computer Programming", "credits": 3},
    {"code": "MA 110",  "title": "Mathematics for Computing I", "credits": 3},
    {"code": "LA 111",  "title": "Communication and Academic Writing Skills", "credits": 3},
    {"code": "BIT 120", "title": "Computer Systems and Architecture", "credits": 3},
    {"code": "MA 120",  "title": "Discrete Mathematics for IT", "credits": 3}
]

COURSES_YEAR_2 = [
    {"code": "BIT 210", "title": "Object-Oriented Programming", "credits": 3},
    {"code": "BIT 211", "title": "Database Management Systems", "credits": 3},
    {"code": "BIT 220", "title": "Data Structures and Algorithms", "credits": 3},
    {"code": "BIT 221", "title": "Systems Analysis and Design", "credits": 3},
    {"code": "BIT 222", "title": "Web Technologies and Applications", "credits": 3},
    {"code": "BIT 223", "title": "Computer Networks I", "credits": 3}
]

COURSES_YEAR_3 = [
    {"code": "BIT 310", "title": "Operating Systems Concepts", "credits": 3},
    {"code": "BIT 311", "title": "Software Engineering Principles", "credits": 3},
    {"code": "BIT 320", "title": "Computer Networks II & Security", "credits": 3},
    {"code": "BIT 321", "title": "Management Information Systems", "credits": 3},
    {"code": "BIT 322", "title": "IT Project Management", "credits": 3},
    {"code": "BIT 323", "title": "Research Methods in IT", "credits": 3}
]

COURSES_YEAR_4 = [
    {"code": "BIT 410", "title": "Information Security and Cryptography", "credits": 3},
    {"code": "BIT 411", "title": "Distributed Systems & Cloud Computing", "credits": 3},
    {"code": "BIT 420", "title": "Wireless and Mobile Computing", "credits": 3},
    {"code": "BIT 421", "title": "E-Commerce and Enterprise Systems", "credits": 3},
    {"code": "BIT 400", "title": "Final Year IT Project / Capstone Dissertation", "credits": 6}
]

GRADE_POINTS = {
    "A+": 4.0, "A": 4.0, "B+": 3.5, "B": 3.0, "C+": 2.5, "C": 2.0, "D+": 1.0, "D": 0.0
}

def generate_grades_for_profile(profile):
    if profile == "DISTINCTION":
        pool = ["A+", "A", "A", "B+", "A+"]
    elif profile == "MERIT":
        pool = ["B+", "B", "A", "B+", "B", "C+"]
    elif profile == "CREDIT":
        pool = ["B", "C+", "B+", "C", "C+"]
    else:
        pool = ["C+", "C", "C", "B", "C+"]
    return pool

def build_student(id_num, full_name, start_year, gender, profile):
    pool = generate_grades_for_profile(profile)
    
    years = []
    course_groups = [
        (start_year, "FIRST YEAR", COURSES_YEAR_1),
        (start_year + 1, "SECOND YEAR", COURSES_YEAR_2),
        (start_year + 2, "THIRD YEAR", COURSES_YEAR_3),
        (start_year + 3, "FOURTH YEAR", COURSES_YEAR_4)
    ]
    
    total_points = 0.0
    total_credits = 0
    
    for yr, label, courses in course_groups:
        year_courses = []
        for c in courses:
            grade = random.choice(pool)
            pts = GRADE_POINTS[grade]
            year_courses.append({
                "code": c["code"],
                "title": c["title"],
                "credits": c["credits"],
                "grade": grade,
                "grade_points": pts
            })
            total_points += pts * c["credits"]
            total_credits += c["credits"]
            
        years.append({
            "academic_year": f"{yr}",
            "level": label,
            "courses": year_courses,
            "comment": "CLEAR PASS"
        })
        
    gpa = round(total_points / total_credits, 2)
    if gpa >= 3.60:
        classification = "DISTINCTION"
    elif gpa >= 3.00:
        classification = "MERIT"
    elif gpa >= 2.50:
        classification = "CREDIT"
    else:
        classification = "SATISFACTORY"
        
    end_year = start_year + 3
    pronoun = "HE" if gender == "M" else "SHE"
    
    return {
        "student_id": id_num,
        "full_name": full_name,
        "gender": gender,
        "pronoun": pronoun,
        "school": "School of Humanities and Social Sciences",
        "programme": "BACHELOR OF SCIENCE IN INFORMATION TECHNOLOGY",
        "start_year": start_year,
        "end_year": end_year,
        "graduation_session": f"{start_year} - {end_year}",
        "gpa": gpa,
        "qualification_class": classification,
        "academic_record": years
    }

def main():
    os.makedirs('data', exist_ok=True)
    
    # 3 Primary reference students
    s1 = build_student("ZOU/2012/0482", "MUKUKA MUTALE", 2012, "M", "DISTINCTION")
    s2 = build_student("ZOU/2013/0119", "CHISANGA BWALYA", 2013, "F", "MERIT")
    s3 = build_student("ZOU/2013/0534", "PHIRI KONDWANI", 2013, "M", "CREDIT")
    
    students = [s1, s2, s3]
    
    # Generate 47 additional students for batch performance testing (total 50)
    first_names = ["Kabwe", "Mwamba", "Lombe", "Chileshe", "Kunda", "Mapalo", "Nason", "Thandiwe", "Bupe", "Natasha", "Mulenga", "Chipo"]
    last_names = ["Zimba", "Banda", "Lungi", "Tembo", "Sikazwe", "Musonda", "Sakala", "Njobvu", "Kapele", "Mwale", "Nyirenda", "Soko"]
    
    profiles = ["DISTINCTION", "MERIT", "CREDIT", "SATISFACTORY"]
    
    for i in range(4, 51):
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        name = f"{ln.upper()} {fn.upper()}"
        id_num = f"ZOU/2013/{i:04d}"
        gender = "F" if fn in ["Thandiwe", "Natasha", "Bupe"] else "M"
        profile = random.choice(profiles)
        students.append(build_student(id_num, name, 2013, gender, profile))
        
    dataset = {
        "institution": "THE ZAMBIAN OPEN UNIVERSITY",
        "authority": "OFFICE OF THE DEPUTY REGISTRAR (ACADEMIC)",
        "programme_code": "BIT",
        "programme_name": "Bachelor of Science in Information Technology",
        "total_records": len(students),
        "students": students
    }
    
    with open('data/test_senate_bit_2012_2017.json', 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
        
    print(f"Generated data/test_senate_bit_2012_2017.json with {len(students)} student records.")

if __name__ == '__main__':
    main()
