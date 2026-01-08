import unittest

from srm.exceptions.NotFoundException import NotFoundException
from srm.exceptions.ValidationException import ValidationException
from srm.repository.in_memory.StudentRepository import StudentRepository
from srm.repository.in_memory.DisciplineRepository import DisciplineRepository
from srm.repository.in_memory.GradeRepository import GradeRepository
from srm.service.Service import Service


class TestServiceStudents(unittest.TestCase):
    def setUp(self):
        self.student_repo = StudentRepository()
        self.discipline_repo = DisciplineRepository()
        self.grade_repo = GradeRepository()
        self.service = Service(self.student_repo, self.discipline_repo, self.grade_repo)

        # base data
        self.service.add_student(1, "Alice")
        self.service.add_student(2, "Bob")
        self.service.add_discipline(10, "Math")

    def test_add_student_saved(self):
        self.service.add_student(3, "Charlie")
        s = self.service.get_student_by_id(3)
        self.assertIsNotNone(s)
        self.assertEqual(s.student_id, 3)
        self.assertEqual(s.name, "Charlie")

    def test_update_student_ok(self):
        self.service.update_student(1, "Alicia")
        self.assertEqual(self.service.get_student_by_id(1).name, "Alicia")

    def test_update_student_not_found_raises(self):
        with self.assertRaises(NotFoundException):
            self.service.update_student(999, "Name")

    def test_update_student_empty_name_raises(self):
        with self.assertRaises(ValidationException):
            self.service.update_student(1, "   ")

    def test_remove_student_cascades_grades(self):
        # give student 1 two grades
        self.service.add_grade(1, 10, 7)
        self.service.add_grade(1, 10, 9)
        # give student 2 one grade
        self.service.add_grade(2, 10, 6)

        removed, backup = self.service.remove_student(1)
        self.assertTrue(removed)
        self.assertEqual(len(backup), 2)
        self.assertTrue(all(g.student_id == 1 for g in backup))

        # student removed
        self.assertIsNone(self.service.get_student_by_id(1))

        # grades for student 1 removed, student 2 grade remains
        remaining = self.service.get_all_grades()
        self.assertEqual(len(remaining), 1)
        self.assertEqual(remaining[0].student_id, 2)

    def test_remove_nonexistent_student_returns_false(self):
        removed, backup = self.service.remove_student(123456)
        self.assertFalse(removed)
        self.assertEqual(backup, [])



