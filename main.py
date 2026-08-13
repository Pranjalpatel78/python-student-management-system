import json
from pathlib import Path

DATA_FILE = Path("students.json")


def load_students():
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read student data. Starting with an empty list.")
        return []


def save_students(students):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(students, file, indent=4)


def get_next_id(students):
    return max((student["id"] for student in students), default=0) + 1


def add_student(students):
    print("\n--- Add Student ---")
    name = input("Name: ").strip()
    course = input("Course: ").strip()
    email = input("Email: ").strip()

    if not name or not course or not email:
        print("All fields are required.")
        return

    if "@" not in email or "." not in email.split("@")[-1]:
        print("Please enter a valid email address.")
        return

    student = {
        "id": get_next_id(students),
        "name": name,
        "course": course,
        "email": email
    }
    students.append(student)
    save_students(students)
    print(f"Student added successfully. ID: {student['id']}")


def view_students(students):
    print("\n--- Student Records ---")
    if not students:
        print("No student records found.")
        return

    print(f"{'ID':<5}{'Name':<25}{'Course':<20}{'Email'}")
    print("-" * 75)
    for student in students:
        print(
            f"{student['id']:<5}"
            f"{student['name'][:23]:<25}"
            f"{student['course'][:18]:<20}"
            f"{student['email']}"
        )


def search_students(students):
    print("\n--- Search Student ---")
    keyword = input("Enter name, course or email: ").strip().lower()

    results = [
        student for student in students
        if keyword in student["name"].lower()
        or keyword in student["course"].lower()
        or keyword in student["email"].lower()
    ]

    if not results:
        print("No matching student found.")
        return

    for student in results:
        print(
            f"ID: {student['id']} | "
            f"Name: {student['name']} | "
            f"Course: {student['course']} | "
            f"Email: {student['email']}"
        )


def update_student(students):
    print("\n--- Update Student ---")
    try:
        student_id = int(input("Enter student ID: "))
    except ValueError:
        print("ID must be a number.")
        return

    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        print("Student not found.")
        return

    name = input(f"Name [{student['name']}]: ").strip()
    course = input(f"Course [{student['course']}]: ").strip()
    email = input(f"Email [{student['email']}]: ").strip()

    if name:
        student["name"] = name
    if course:
        student["course"] = course
    if email:
        if "@" not in email or "." not in email.split("@")[-1]:
            print("Invalid email. Update cancelled.")
            return
        student["email"] = email

    save_students(students)
    print("Student updated successfully.")


def delete_student(students):
    print("\n--- Delete Student ---")
    try:
        student_id = int(input("Enter student ID: "))
    except ValueError:
        print("ID must be a number.")
        return

    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        print("Student not found.")
        return

    students.remove(student)
    save_students(students)
    print("Student deleted successfully.")


def main():
    students = load_students()

    while True:
        print("\n" + "=" * 40)
        print("     PYTHON STUDENT MANAGEMENT SYSTEM")
        print("=" * 40)
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            view_students(students)
        elif choice == "3":
            search_students(students)
        elif choice == "4":
            update_student(students)
        elif choice == "5":
            delete_student(students)
        elif choice == "6":
            print("Thank you for using the Student Management System.")
            break
        else:
            print("Invalid choice. Please select 1-6.")


if __name__ == "__main__":
    main()
