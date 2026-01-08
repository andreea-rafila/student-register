from faker import Faker
from srm.model.Discipline import Discipline
from srm.model.Grade import Grade
from srm.model.Student import Student
from srm.repository.abstracts.AbstractDisciplineRepository import AbstractDisciplineRepository
from srm.repository.abstracts.AbstractGradeRepository import AbstractGradeRepository
from srm.repository.abstracts.AbstractStudentRepository import AbstractStudentRepository
from srm.exceptions.NotFoundException import NotFoundException
from srm.exceptions.ValidationException import ValidationException


class Service:
    def __init__(self, student_repo: AbstractStudentRepository, discipline_repo: AbstractDisciplineRepository, grade_repo: AbstractGradeRepository):
        self.student_repo = student_repo
        self.discipline_repo = discipline_repo
        self.grade_repo = grade_repo

    def add_student(self, student_id: int, name: str) -> None:
        student = Student(student_id= student_id, name=name)
        self.student_repo.save(student)

    def update_student(self, student_id: int, new_name: str) -> None:
        student = self.student_repo.find_one(student_id)
        if student is None:
            raise NotFoundException(f"Student with id {student_id} not found")
        if new_name.strip() == "":
            raise ValidationException("Student name cannot be empty")
        student.name = new_name
        self.student_repo.save(student)

    def remove_student(self, student_id: int) -> tuple[bool, list[Grade]]:
        deleted_something = self.student_repo.remove(student_id)
        grade_backup = []
        if deleted_something:
            grade_backup = self.grade_repo.remove_by_student(student_id)
        return deleted_something, grade_backup

    def get_student_by_id(self, student_id: int) -> Student:
        return self.student_repo.find_one(student_id)

    def get_students_by_name(self, name: str) -> list[Student]:
        return self.student_repo.find_by_name(name)

    def add_discipline(self, discipline_id: int, name: str) -> None:
        discipline = Discipline(discipline_id=discipline_id, name=name)
        self.discipline_repo.save(discipline)

    def update_discipline(self, discipline_id: int, new_name: str) -> None:
        discipline = self.discipline_repo.find_one(discipline_id)
        if discipline is None:
            raise NotFoundException(f"Discipline with id {discipline_id} not found")
        if new_name.strip() == "":
            raise ValidationException("Discipline name cannot be empty")
        discipline.name = new_name
        self.discipline_repo.save(discipline)

    def remove_discipline(self, discipline_id: int) -> tuple[bool, list[Grade]]:
        deleted_something = self.discipline_repo.remove(discipline_id)
        grade_backup = []
        if deleted_something:
            grade_backup = self.grade_repo.remove_by_discipline(discipline_id)
        return deleted_something, grade_backup

    def get_discipline_by_id(self, discipline_id: int) -> Discipline:
        return self.discipline_repo.find_one(discipline_id)

    def get_disciplines_by_name(self, name: str) -> list[Discipline]:
        return self.discipline_repo.find_by_name(name)

    def add_grade(self, student_id: int, discipline_id: int, grade_value: int) -> None:
        if self.student_repo.find_one(student_id) is None:
            raise NotFoundException(f"Student with id {student_id} not found")
        if self.discipline_repo.find_one(discipline_id) is None:
            raise NotFoundException(f"Discipline with id {discipline_id} not found")
        if not (1 <= grade_value <= 10):
            raise ValidationException("Grade must be between 1 and 10")
        grade = Grade(student_id=student_id, discipline_id=discipline_id, grade_value=grade_value)
        self.grade_repo.save(grade)

    def get_grades_by_student(self, student_id: int) -> list[Grade]:
        return self.grade_repo.find_by_student(student_id)

    def get_grades_by_discipline(self, discipline_id: int) -> list[Grade]:
        return self.grade_repo.find_by_discipline(discipline_id)

    def get_all_grades(self) -> list[Grade]:
        return self.grade_repo.find_all()

    def remove_grade(self, student_id: int, discipline_id: int, grade_value: int) -> bool:
        return self.grade_repo.remove_grade(student_id=student_id, discipline_id=discipline_id, grade_value=grade_value)

    def stat_1(self) -> list[Student]:
        # all students failing at least one discipline
        # fail = avg grade < 5

        # if there are no grades for a discipline, the student is failing that discipline
        # for each student, check all disciplines
        # get the grades of the student at that discipline and compute the average
        # if avg < 5, the student is failing that discipline

        failing_students = []
        for student in self.student_repo.find_all():
            for discipline in self.discipline_repo.find_all():
                discipline_grades = self.grade_repo.find_by_discipline(discipline.discipline_id) # get all grades for that discipline, for all students
                student_grades = [grade.grade_value for grade in discipline_grades if grade.student_id == student.student_id] # filter grades for the current student
                if len(student_grades) > 0:
                    avg_grade = sum(student_grades) / len(student_grades)
                    if avg_grade < 5:
                        failing_students.append(student)
                        break
                else:
                    failing_students.append(student)
                    break
        return failing_students

    def stat_2(self) -> dict[Student, float]:
        # all students sorted by their aggregate average grade (descending)
        # if a student has no grades, their average is considered 0

        situation = {}
        for student in self.student_repo.find_all():
            aggregate_grades = []

            for discipline in self.discipline_repo.find_all():
                discipline_grades = self.grade_repo.find_by_discipline(discipline.discipline_id) # get all grades for that discipline, for all students
                student_grades = [grade.grade_value for grade in discipline_grades if grade.student_id == student.student_id] # filter grades for the current student

                avg_grade = 0
                if len(student_grades) > 0:
                    avg_grade = sum(student_grades) / len(student_grades)

                aggregate_grades.append(avg_grade)

            overall_avg = 0
            if len(aggregate_grades) > 0:
                overall_avg = sum(aggregate_grades) / len(aggregate_grades)

            situation[student] = overall_avg

        situation = dict(sorted(situation.items(), key=lambda item: item[1], reverse=True))
        return situation

    def stat_3(self) -> dict[Discipline, float]:
        # for all disciplines with at least one grade, their average grade (descending)
        situation = {}

        for discipline in self.discipline_repo.find_all():
            discipline_grades = self.grade_repo.find_by_discipline(discipline.discipline_id)
            if len(discipline_grades) > 0:
                grade_sum = 0
                for grade in discipline_grades:
                    grade_sum += grade.grade_value
                avg_grade = grade_sum / len(discipline_grades)
                situation[discipline] = avg_grade

        situation = dict(sorted(situation.items(), key=lambda item: item[1], reverse=True))

        return situation

    def populate_example_data(self) -> None:
        fake = Faker()
        # 20 students
        for i in range(1, 21):
            name = fake.name()
            self.add_student(i, name)
        # 20 disciplines
        for i in range(1, 21):
            name = fake.word().capitalize()
            self.add_discipline(i, name)
        # 20 random grades
        import random
        for _ in range(400):
            student_id = random.randint(1, 20)
            discipline_id = random.randint(1, 20)
            grade_value = random.randint(4, 10)
            self.add_grade(student_id, discipline_id, grade_value)







