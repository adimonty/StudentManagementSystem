import csv
from typing import List

class Student:

    def create(self, f_name, l_name, stdnt_id):
        self.f_name = f_name
        self.l_name = l_name
        self.stdnt_id = stdnt_id
        self._courses = []  # Private list to store enrolled courses
        self._grades = {}  # Private dictionary to store grades for each course

    def enroll_in_course(self, course):
        self._courses.append(course)

    def add_grade(self, course_name, grade):
        self._grades[course_name] = grade

    def get_courses(self):
        return self._courses

    def get_grades(self):
        return self._grades

    def calculate_avg_grade(self):
        if len(self._grades) == 0:
            return 0

        total_grade = sum(self._grades.values())
        return total_grade / len(self._grades)

    def get_full_name(self) -> str:
        # join the first name and last name for full name
        return f"{self.f_name} {self.l_name}"

    def to_csv_row(self, course_records: List[str]) -> List[str]:
        row = [self.f_name, self.l_name, str(self.stdnt_id)]

        # Append course name and matched grade to row
        for course_name in course_records:
            row.append(course_name)
            if course_name in self._grades:
                row.append(str(self._grades[course_name]))
            else:
                row.append('')

        # Add average grade to row
        row.append(str(self.calculate_avg_grade()))
        return row


class SchoolSystem:
    def create(self):
        self.students = {}
        self.courses = []

    def add_student(self, f_name, l_name, stdnt_id):
        student = self.create_student(f_name, l_name, stdnt_id)
        self.students[stdnt_id] = student
        print(f"Student '{f_name} {l_name}' with ID '{stdnt_id}' has been added.")

    def create_student(self, f_name, l_name, stdnt_id):
        return {
            'f_name': f_name,
            'l_name': l_name,
            'stdnt_id': stdnt_id,
            'courses': [],
            'grades': {}
        }

    def add_course(self, course_name):
        self.courses.append(course_name)
        print(f"Course '{course_name}' has been added.")

    def enroll_student(self, stdnt_id: int, course_name: str) -> None:
        if stdnt_id in self.students:
            if course_name in self.courses:
                student = self.students[stdnt_id]
                student['courses'].append(course_name)
                print(f"Student '{student['f_name']} {student['l_name']}' has been enrolled in '{course_name}'.")
            else:
                raise ValueError("Student or course not found.")

    def add_grade(self, stdnt_id: int, course_name: str, grade: float) -> None:
        if stdnt_id in self.students:
            if course_name in self.courses:
                student = self.students[stdnt_id]
                student['grades'][course_name] = grade
                print(f"Grade '{grade}' has been added for student '{student['f_name']} {student['l_name']}' in '{course_name}'.")
            else:
                print(f"Course '{course_name}' not found.")
        else:
            print(f"Student with ID '{stdnt_id}' not found.")

    def calculate_avg_grade(self, stdnt_id: int) -> float:
        if stdnt_id in self.students:
            student = self.students[stdnt_id]
            grades = student['grades']
            if grades:
                total_grade = sum(grades.values())
                return total_grade / len(grades)
            else:
                return 0.0
        else:
            print(f"Student with ID '{stdnt_id}' not found.")
            return None

    def save_to_csv(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            header = ['First Name', 'Last Name', 'Student ID'] + self.courses + ['Average Grade']
            writer.writerow(header)

            for stdnt_id, student in self.students.items():
                row = [student['f_name'], student['l_name'], str(student['stdnt_id'])]
                grades = student['grades']
                for course in self.courses:
                    if course in grades:
                        row.append(str(grades[course]))
                    else:
                        row.append('')
                row.append(str(self.calculate_avg_grade(stdnt_id)))
                writer.writerow(row)

        print(f"Student information and grades have been successfully saved to '{filename}'.")

    def show_avg_grade(self, stdnt_id: int):
        avg_grade = self.calculate_avg_grade(stdnt_id)
        if avg_grade is not None:
            student = self.students.get(stdnt_id)
            if student:
                print(f"The average grade for student '{student['f_name']} {student['l_name']}' is {avg_grade:.2f}")
            else:
                print(f"Student with ID '{stdnt_id}' not found.")



# Example
school = SchoolSystem()
school.create()

school.add_student("Andrea", "Pirlo", 123)
school.add_student("Thierry", "Henry", 456)

school.add_course("Maths")
school.add_course("History")
school.add_course("Geography")
school.add_course("Science")

school.enroll_student(123, "Maths")
school.enroll_student(123, "History")
school.enroll_student(456, "Geography")
school.enroll_student(456, "Science")

school.add_grade(123, "Maths", 65)
school.add_grade(123, "History", 73)
school.add_grade(456, "Geography", 81)
school.add_grade(456, "Science", 67)

school.show_avg_grade(123)
school.show_avg_grade(456)

school.save_to_csv('student_records.csv')
