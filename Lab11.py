"""
[DATA STORAGE FORMATTING NOTES]
Students.txt: idFirstName LastName
Assignments.txt: title 
                 id
                 points
Submission(.txt): studentId|assignmentId|grade (percent)
"""
import os
def get_assignments():
    assignments_points_map = {}
    with open("data/assignments.txt", "r") as data:
        lines = data.readlines()
        for i in range(0, len(lines), 3):
            title, _id, points = lines[i], lines[i+1], lines[i+2]
            assignments_points_map[_id.strip()] = {"points": int(points.strip()), "title": title.strip()}
        data.close()
    return assignments_points_map

def find_assignment_id_by_title(assignments, title):
    for _id, data in students.items():
        if data.get("title") == title: return _id

def get_students():
    students = {}
    with open("data/students.txt", "r") as data:
        lines = data.readlines()
        for student in lines:
            _id, name = student[:3], student[3:]
            students[name.strip()] = _id.strip()
        data.close()
    return students


# def find_student_id_by_name(students, name):
#     for _id, _name in students.items():
#         if _name == name: return _id

def print_menu():
    print("\
1. Student grade\n\
2. Assignment statistics\n\
3. Assignment graph\n")

def find_student_grade(students, assignments):
    student_name = input("What is the student's name: ")
    student_id = students.get(student_name)
    if not student_id: return

    total_points = 0
    for f in os.listdir("./data/submissions"):
        with open(os.path.join("data/submissions", f)) as submission:
            data = submission.readline().split("|")
            if not int(data[0]) == int(student_id):
                submission.close()
                continue
            assignment_id, grade = data[1].strip(), data[2].strip()
            assignment = assignments.get(assignment_id)
            if not assignment: continue

            points_earned = (int(grade)/100)*int(assignment.get("points"))
            total_points += points_earned
            submission.close()

    student_grade = int(total_points / 10)
    print(f"{student_grade}%")
    return student_grade
    

def main():
    students, assignments = get_students(), get_assignments()
    print_menu()
    selection = int(input("Enter your selection: "))

    match selection:
        case 1:
            find_student_grade(students, assignments)
        case 2:
            pass
        case 3:
            pass

if __name__ == "__main__":
    main()