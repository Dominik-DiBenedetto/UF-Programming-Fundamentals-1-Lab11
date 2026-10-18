"""
[DATA STORAGE FORMATTING NOTES]
Students.txt: idFirstName LastName
Assignments.txt: title 
                 id
                 points
Submission(.txt): studentId|assignmentId|grade (percent)
"""
import os
import matplotlib.pyplot as plt

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
    for _id, data in assignments.items():
        if data.get("title") == title: return _id

def get_assignment_grades(assignments, submission_paths):
    assignment_name = input("What is the assignment name: ")
    assignment_id = find_assignment_id_by_title(assignments, assignment_name)
    assignment = assignments.get(assignment_id)
    if not assignment:
        print("Assignment not found")
        return

    grades = []
    for path in submission_paths:
        with open(path, "r") as submission:
            data = submission.readline().split("|")
            if data[1] != assignment_id: continue
            grade = int(data[2])
            grades.append(grade)
    return grades, assignment_name

def get_students():
    students = {}
    with open("data/students.txt", "r") as data:
        lines = data.readlines()
        for student in lines:
            _id, name = student[:3], student[3:]
            students[name.strip()] = _id.strip()
        data.close()
    return students

def get_submission_paths():
    paths = []
    for f in os.listdir("./data/submissions"):
        paths.append(os.path.join("data/submissions", f))
    return paths

# def find_student_id_by_name(students, name):
#     for _id, _name in students.items():
#         if _name == name: return _id

def print_menu():
    print("\
1. Student grade\n\
2. Assignment statistics\n\
3. Assignment graph\n")

def find_student_grade(students, assignments, submission_paths):
    student_name = input("What is the student's name: ")
    student_id = students.get(student_name)
    if not student_id: 
        print("Student not found")
        return

    total_points = 0
    for path in submission_paths:
        with open(path) as submission:
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

    student_grade = round(total_points / 10)
    print(f"{student_grade}%")
    return student_grade
    
def calculate_assignment_average(assignments, submission_paths):
    grades, _ = get_assignment_grades(assignments, submission_paths)
    
    print(f"Min: {min(grades)}%")
    print(f"Avg: {int(sum(grades)/len(grades))}%")
    print(f"Max: {max(grades)}%")   

def plot_assignment_graph(assignments, submission_paths):
    grades, assignment_name = get_assignment_grades(assignments, submission_paths)
    plt.hist(grades, bins=[0,10,20,30,40,50,60,70,80,90,100])
    plt.title(f"Grade distribution for {assignment_name}")
    plt.show()


def main():
    students, assignments, submission_paths = get_students(), get_assignments(), get_submission_paths()
    print_menu()
    selection = int(input("Enter your selection: "))

    match selection:
        case 1:
            find_student_grade(students, assignments, submission_paths)
        case 2:
            calculate_assignment_average(assignments, submission_paths)
        case 3:
            plot_assignment_graph(assignments, submission_paths)

if __name__ == "__main__":
    main()