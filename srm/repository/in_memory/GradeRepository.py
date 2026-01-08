from srm.model.Grade import Grade
from srm.repository.abstracts.AbstractGradeRepository import AbstractGradeRepository


class GradeRepository(AbstractGradeRepository):
    def __init__(self):
        self._grades = []

    def find_all(self) -> list[Grade]:
        return self._grades

    def save(self, grade: Grade) -> None:
        self._grades.append(grade)

    def find_by_student(self, student_id: int) -> list[Grade]:
        aux = []
        for grade in self._grades:
            if grade.student_id == student_id:
                aux.append(grade)

        return aux

    def find_by_discipline(self, discipline_id: int) -> list[Grade]:
        aux = []
        for grade in self._grades:
            if grade.discipline_id == discipline_id:
                aux.append(grade)

        return aux

    def remove_by_student(self, student_id:int) -> list[Grade]:
        aux = []
        was_removed = []

        for grade in self._grades:
            if grade.student_id != student_id:
                aux.append(grade)
            else:
                was_removed.append(grade)

        self._grades = aux
        return was_removed

    def remove_by_discipline(self, discipline_id:int) -> list[Grade]:
        aux = []
        was_removed = []

        for grade in self._grades:
            if grade.discipline_id != discipline_id:
                aux.append(grade)
            else:
                was_removed.append(grade)

        self._grades = aux
        return was_removed

    def remove_grade(self, student_id: int, discipline_id: int, grade_value: int) -> bool:
        for grade in self._grades:
            if grade.discipline_id == discipline_id and grade.student_id == student_id and grade.grade_value == grade_value:
                self._grades.remove(grade)
                return True
        return False


