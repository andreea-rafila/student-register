import unittest

from srm.exceptions.NotFoundException import NotFoundException
from srm.exceptions.ValidationException import ValidationException
from srm.repository.in_memory.StudentRepository import StudentRepository
from srm.repository.in_memory.DisciplineRepository import DisciplineRepository
from srm.repository.in_memory.GradeRepository import GradeRepository
from srm.service.Service import Service


class TestServiceGradesValidation(unittest.TestCase):
    def setUp(self):
        self.service = Service(StudentRepository(), DisciplineRepository(), GradeRepository())
        self.service.add_student(1, "Alice")
        self.service.add_discipline(10, "Math")

    def test_add_grade_ok(self):
        self.service.add_grade(1, 10, 8)
        grades = self.service.get_all_grades()
        self.assertEqual(len(grades), 1)
        self.assertEqual(grades[0].grade_value, 8)

    def test_add_grade_student_not_found(self):
        with self.assertRaises(NotFoundException):
            self.service.add_grade(999, 10, 8)

    def test_add_grade_discipline_not_found(self):
        with self.assertRaises(NotFoundException):
            self.service.add_grade(1, 999, 8)

    def test_add_grade_invalid_value(self):
        with self.assertRaises(ValidationException):
            self.service.add_grade(1, 10, 0)
        with self.assertRaises(ValidationException):
            self.service.add_grade(1, 10, 11)
