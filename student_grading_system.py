"""
Student Grading System

Uses: variables, functions, if-elif-else, for/while loops, lists, tuples,
      sets, dictionaries and the random module.
"""

import random

SUBJECTS = ("Maths", "Physics", "Programming", "English", "Chemistry")
students = {}   # roll number -> {"name": ..., "marks": [...]}


# ---------- helper functions ----------
def new_roll():
    """Random roll number like 22BCE1234 that is not already used."""
    roll = "22BCE" + str(random.randint(1000, 9999))
    while roll in students:
        roll = "22BCE" + str(random.randint(1000, 9999))
    return roll


def average(marks):
    return sum(marks) / len(marks)


def grade(avg):
    if avg >= 90:
        return "A"
    elif avg >= 80:
        return "B"
    elif avg >= 70:
        return "C"
    elif avg >= 60:
        return "D"
    elif avg >= 50:
        return "E"
    return "F"


def result(marks):
    """FAIL if any subject is below 40."""
    return "FAIL" if min(marks) < 40 else "PASS"


def read_number(prompt, low, high):
    """Keep asking until the user enters a whole number from low to high."""
    while True:
        text = input(prompt)
        if text.isdigit() and low <= int(text) <= high:
            return int(text)
        print("Please enter a whole number from", low, "to", high)


def ask_roll():
    """Ask for a roll number; return None if it does not exist."""
    roll = input("Enter roll number : ").strip().upper()
    if roll in students:
        return roll
    print("Roll number not found.")
    return None


def show_rows(rolls):
    """Print a table for the given roll numbers."""
    if not rolls:
        print("No student records available.")
        return
    print("-" * 70)
    print(f"{'ROLL NO':<12}{'NAME':<18}{'TOTAL':<8}{'AVG':<8}{'GRADE':<8}RESULT")
    print("-" * 70)
    for roll in rolls:
        name, marks = students[roll]["name"], students[roll]["marks"]
        avg = average(marks)
        print(f"{roll:<12}{name[:16]:<18}{sum(marks):<8}{avg:<8.2f}"
              f"{grade(avg):<8}{result(marks)}")
    print("-" * 70)


def averages():
    """List of (average, roll) pairs for all students."""
    return [(average(s["marks"]), r) for r, s in students.items()]


# ---------- menu operations ----------
def add_student():
    name = input("Enter student name : ").strip()
    if name == "":
        print("Name cannot be empty.")
        return
    marks = [read_number("  Marks in " + sub + " (0-100) : ", 0, 100)
             for sub in SUBJECTS]
    roll = new_roll()
    students[roll] = {"name": name, "marks": marks}
    print("Student added. Roll number:", roll)


def marksheet():
    roll = ask_roll()
    if roll is None:
        return
    marks = students[roll]["marks"]
    avg = average(marks)
    print("\n" + "=" * 30)
    print(roll, "-", students[roll]["name"])
    print("=" * 30)
    for i in range(len(SUBJECTS)):
        print(f"{SUBJECTS[i]:<20}{marks[i]:>5}")
    print("-" * 30)
    print(f"{'Total':<20}{sum(marks):>5}")
    print(f"{'Average':<20}{avg:>5.2f}")
    print(f"{'Grade':<20}{grade(avg):>5}")
    print(f"{'Result':<20}{result(marks):>5}\n")


def update_marks():
    roll = ask_roll()
    if roll is None:
        return
    for i in range(len(SUBJECTS)):
        print(" ", i + 1, SUBJECTS[i])
    i = read_number("Choose subject number : ", 1, len(SUBJECTS)) - 1
    students[roll]["marks"][i] = read_number("  New marks (0-100) : ", 0, 100)
    print("Marks updated.")


def delete_student():
    roll = ask_roll()
    if roll is not None:
        del students[roll]
        print("Record deleted.")


def topper():
    if not students:
        print("No student records available.")
        return
    avg, roll = max(averages())
    print(f"Topper: {students[roll]['name']} ({roll}) with average {avg:.2f}")


def grade_distribution():
    counts = {}
    for avg, roll in averages():
        g = grade(avg)
        counts[g] = counts.get(g, 0) + 1
    for g in sorted(counts):
        print("Grade", g, ":", "*" * counts[g], f"({counts[g]})")


def pass_fail():
    passed = [r for r in students if result(students[r]["marks"]) == "PASS"]
    failed = [r for r in students if r not in passed]
    print("Passed:", passed)
    print("Failed:", failed)


def unique_averages():
    values = sorted(round(avg, 2) for avg, roll in averages())
    print("Sorted averages :", values)
    print("Unique averages :", sorted(set(values)))


def kth_smallest():
    if not students:
        print("No student records available.")
        return
    k = read_number("Enter K : ", 1, len(students))
    avg, roll = sorted(averages())[k - 1]
    print(f"{k}th smallest average: {avg:.2f} - {students[roll]['name']} ({roll})")


def statistics():
    if not students:
        print("No student records available.")
        return
    values = [avg for avg, roll in averages()]
    print("Students        :", len(values))
    print("Class average   :", round(sum(values) / len(values), 2))
    print("Highest average :", round(max(values), 2))
    print("Lowest average  :", round(min(values), 2))


def load_samples():
    samples = [("Aadya Singh", [95, 88, 97, 91, 89]),
               ("Rahul Verma", [72, 65, 80, 70, 68]),
               ("Meera Nair", [55, 38, 60, 52, 49]),
               ("Kabir Khan", [84, 79, 88, 82, 85]),
               ("Ishita Rao", [72, 65, 80, 70, 68])]
    for name, marks in samples:
        students[new_roll()] = {"name": name, "marks": marks}
    print(len(samples), "sample records loaded.")


# ---------- main program ----------
MENU = """
============ STUDENT GRADING SYSTEM ============
 1. Add a student              8. Grade distribution
 2. Display all students       9. Pass / fail lists
 3. Show mark sheet           10. Sorted and unique averages
 4. Update marks              11. Kth smallest average
 5. Delete a student          12. Class statistics
 6. Find the topper           13. Load sample data
 7. Show in reverse order      0. Exit
================================================"""

while True:
    print(MENU)
    choice = input("Enter your choice : ").strip()
    if choice == "1":
        add_student()
    elif choice == "2":
        show_rows(list(students))
    elif choice == "3":
        marksheet()
    elif choice == "4":
        update_marks()
    elif choice == "5":
        delete_student()
    elif choice == "6":
        topper()
    elif choice == "7":
        show_rows(list(students)[::-1])
    elif choice == "8":
        grade_distribution()
    elif choice == "9":
        pass_fail()
    elif choice == "10":
        unique_averages()
    elif choice == "11":
        kth_smallest()
    elif choice == "12":
        statistics()
    elif choice == "13":
        load_samples()
    elif choice == "0":
        print("Thank you for using the Student Grading System.")
        break
    else:
        print("Invalid choice. Please enter a number from the menu.")