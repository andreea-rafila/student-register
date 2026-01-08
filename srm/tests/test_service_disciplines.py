import unittest

from srm.exceptions.NotFoundException import NotFoundException
from srm.exceptions.ValidationException import ValidationException
from srm.repository.in_memory.StudentRepository import StudentRepository
from srm.repository.in_memory.DisciplineRepository import DisciplineRepository
from srm.repository.in_memory.GradeRepository import GradeRepository
from srm.service.Service import Service


class TestServiceDisciplines(unittest.TestCase):
    def setUp(self):
        self.student_repo = StudentRepository()
        self.discipline_repo = DisciplineRepository()
        self.grade_repo = GradeRepository()
        self.service = Service(self.student_repo, self.discipline_repo, self.grade_repo)

        self.service.add_student(1, "Alice")
        self.service.add_student(2, "Bob")
        self.service.add_discipline(10, "Math")
        self.service.add_discipline(20, "Info")

    def test_add_discipline_saved(self):
        self.service.add_discipline(30, "Physics")
        d = self.service.get_discipline_by_id(30)
        self.assertIsNotNone(d)
        self.assertEqual(d.discipline_id, 30)
        self.assertEqual(d.name, "Physics")

    def test_update_discipline_ok(self):
        self.service.update_discipline(10, "Mathematics")
        self.assertEqual(self.service.get_discipline_by_id(10).name, "Mathematics")

    def test_update_discipline_not_found_raises(self):
        with self.assertRaises(NotFoundException):
            self.service.update_discipline(999, "X")

    def test_update_discipline_empty_name_raises(self):
        with self.assertRaises(ValidationException):
            self.service.update_discipline(10, "   ")

    def test_remove_discipline_cascades_grades(self):
        self.service.add_grade(1, 10, 7)
        self.service.add_grade(2, 10, 8)
        self.service.add_grade(2, 20, 9)

        removed, backup = self.service.remove_discipline(10)
        self.assertTrue(removed)
        self.assertEqual(len(backup), 2)
        self.assertTrue(all(g.discipline_id == 10 for g in backup))

        # discipline removed
        self.assertIsNone(self.service.get_discipline_by_id(10))

        # grades at discipline 10 removed, discipline 20 grades remain
        remaining = self.service.get_all_grades()
        self.assertEqual(len(remaining), 1)
        self.assertEqual(remaining[0].discipline_id, 20)

    def test_remove_nonexistent_discipline_returns_false(self):
        removed, backup = self.service.remove_discipline(123456)
        self.assertFalse(removed)
        self.assertEqual(backup, [])

