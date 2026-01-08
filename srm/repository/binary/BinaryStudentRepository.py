import pickle
from pathlib import Path

from srm.model.Student import Student
from srm.repository.abstracts.AbstractStudentRepository import AbstractStudentRepository


class BinaryStudentRepository(AbstractStudentRepository):
    def __init__(self, file_path: str):
        self._file_path = Path(file_path)
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        self._students: dict[int, Student] = {}
        self._load_from_file()


    def find_all(self) -> list[Student]:
        return list(self._students.values())

    def find_one(self, student_id: int) -> Student:
        return self._students.get(student_id)

    def save(self, student: Student) -> None:
        self._students[student.student_id] = student
        self._write_to_file()

    def remove(self, student_id: int) -> bool:
        if student_id not in self._students:
            return False
        self._students.pop(student_id)
        self._write_to_file()
        return True

    def _load_from_file(self) -> None:
        if not self._file_path.exists():
            return

        with self._file_path.open("rb") as f:
            self._students = pickle.load(f)

    def _write_to_file(self) -> None:
        #srm/repository/binary/student.bin
        with self._file_path.open("wb") as f:
            pickle.dump(self._students, f)

    def find_by_name(self, name: str) -> list[Student]:
        result = []
        for student in self._students.items():
            if name.lower() in student[1].name.lower():
                result.append(student[1])
        return result
