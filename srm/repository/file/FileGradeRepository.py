import json
from pathlib import Path

from srm.model.Grade import Grade
from srm.repository.abstracts.AbstractGradeRepository import AbstractGradeRepository


class FileGradeRepository(AbstractGradeRepository):
    def __init__(self, file_path: str):
        self._file_path = Path(file_path)
        self._grades = []
        self._load_from_file()

    def find_all(self) -> list[Grade]:
        return self._grades

    def save(self, grade: Grade) -> None:
        self._grades.append(grade)
        self._write_to_file()

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
        self._write_to_file()
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
        self._write_to_file()
        return was_removed

    def _load_from_file(self) -> None:
        if not self._file_path.exists():
            return

        with self._file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        for item in data:
            grade = Grade(
                student_id=item["student_id"],
                discipline_id=item["discipline_id"],
                grade_value=item["grade_value"]
            )
            self._grades.append(grade)

    def _write_to_file(self) -> None:
        data = [
            {
                "student_id": grade.student_id,
                "discipline_id": grade.discipline_id,
                "grade_value": grade.grade_value
            }
            for grade in self._grades
        ]

        # srm/repository/file/grade.json
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        with self._file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def remove_grade(self, student_id: int, discipline_id: int, grade_value: int) -> bool:
        for grade in self._grades:
            if grade.discipline_id == discipline_id and grade.student_id == student_id and grade.grade_value == grade_value:
                self._grades.remove(grade)
                self._write_to_file()
                return True
        return False

