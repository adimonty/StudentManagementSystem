import csv

class Student:
    def create(self, first_name, last_name, student_id):
        # Initialize student attributes
        self.first_name = first_name
        self.last_name = last_name
        self.student_id = student_id
        self.courses = []  # List to store enrolled courses
        self.grades = {}  # Dictionary to store grades for each course

    def enroll_in_course(self, course):
        self.courses.append(course)

    def add_grade(self, course_name, grade):
        self.grades[course_name] = grade

    def calculate_average_grade(self):
        if len(self.grades) == 0:
            return 0

        total_grade = sum(self.grades.values())
        return total_grade / len(self.grades)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def to_csv_row(self, course_records):
        row = [self.first_name, self.last_name, str(self.student_id)]
        for course_name in course_records:
            row.append(course_name)
            if course_name in self.grades:
                row.append(str(self.grades[course_name]))
            else:
                row.append('')
        row.append(str(self.calculate_average_grade()))
        return row


class SchoolSystem:
    def create(self):
        self.student_records = []
        self.course_records = []

    def add_student(self, first_name, last_name, student_id):
        student = Student()
        student.create(first_name, last_name, student_id)
        self.student_records.append(student)

    def add_course(self, course_name):
        self.course_records.append(course_name)

    def enroll_student(self, student_id, course_name):
        student = self.find_student(student_id)

        if student and course_name in self.course_records:
            student.enroll_in_course(course_name)
            print(f"Successfully enrolled student '{student.get_full_name()}' in the course '{course_name}'.")
        else:
            print("Unable to enroll student or course not found.")

    def add_grade(self, student_id, course_name, grade):
        student = self.find_student(student_id)
        if student and course_name in self.course_records:
            student.add_grade(course_name, grade)
            print(f"Added grade '{grade}' for student '{student.get_full_name()}' in the course '{course_name}'.")
        else:
            print("Unable to add grade or student/course not found.")

    def find_student(self, student_id):
        for student in self.student_records:
            if student.student_id == student_id:
                return student
        return None

    def save_to_csv(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            header = ['First Name', 'Last Name', 'Student ID'] + self.course_records + ['Average Grade']
            writer.writerow(header)

            for student in self.student_records:
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