# -*- coding: utf-8 -*-
"""Student_Information_Management_System.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oruy1CzNcmoIy65zW9SUlUwUL-7uDadS
"""

import csv
from typing import List

class Student:

    def create(self, first_name, last_name, student_id):
        self.first_name = first_name
        self.last_name = last_name
        self.student_id = student_id
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

    def calculate_average_grade(self):
        if len(self._grades) == 0:
            return 0

        total_grade = sum(self._grades.values())
        return total_grade / len(self._grades)

    def get_full_name(self) -> str:
        # join the first name and last name to make the full name
        return f"{self.first_name} {self.last_name}"

    def to_csv_row(self, course_records: List[str]) -> List[str]:
        row = [self.first_name, self.last_name, str(self.student_id)]

        # Append course names and corresponding grades to row
        for course_name in course_records:
            row.append(course_name)
            if course_name in self._grades:
                row.append(str(self._grades[course_name]))
            else:
                row.append('')

        # Add average grades to the row
        row.append(str(self.calculate_average_grade()))
        return row


class SchoolSystem:
    def create(self):
        self.student_records = {}  # A dictionary that stores student records and uses student IDs as keys
        self.course_records = []  # A list that stores course records

    def add_student(self, first_name, last_name, student_id):
        student = Student()
        student.create(first_name, last_name, student_id)
        self.student_records[student_id] = student

    def add_course(self, course_name):
        self.course_records.append(course_name)

    def enroll_student(self, student_id: int, course_name: str) -> None:
        student = self.find_student(student_id)

        if student and course_name in self.course_records:
            try:
                student.enroll_in_course(course_name)
                print(f"Student '{student.get_full_name()}' has been enrolled in the course '{course_name}'.")
            except Exception as e:
                print(f"Error occurred while enrolling student: {str(e)}")
        else:
            print("Student or course not found.")

    def add_grade(self, student_id: int, course_name: str, grade: float) -> None:
        student = self.find_student(student_id)
        if student and course_name in self.course_records:
            try:
                student.add_grade(course_name, grade)
                print(f"Grade '{grade}' has been added for the student '{student.get_full_name()}' in the course '{course_name}'.")
            except Exception as e:
                print(f"Error occurred while adding grade: {str(e)}")
        else:
            print("Student or course not found.")


    def find_student(self, student_id):
        if student_id in self.student_records:
            return self.student_records[student_id]
        return None

    def save_to_csv(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            header = ['First Name', 'Last Name', 'Student ID'] + self.course_records + ['Average Grade']
            writer.writerow(header)

            for student_id, student in self.student_records.items():
                writer.writerow(student.to_csv_row(self.course_records))

        print(f"Student information and grades have been successfully saved to '{filename}'.")

    def show_average_grade(self, student_id):
        student = self.find_student(student_id)
        if student:
            average_grade = student.calculate_average_grade()
            print(f"The average grade for student '{student.get_full_name()}' is {average_grade:.2f}")
        else:
            print("Student not found.")


# Example usage
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

school.show_average_grade(123)
school.show_average_grade(456)

school.save_to_csv('student_records.csv')