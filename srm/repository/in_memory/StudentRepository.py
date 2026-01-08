from srm.model.Student import Student
from srm.repository.abstracts.AbstractStudentRepository import AbstractStudentRepository


class StudentRepository(AbstractStudentRepository):
    def __init__(self):
        self._students: dict[int, Student] = {}

    def find_all(self) -> list[Student]:
        return list(self._students.values())

    def find_one(self, student_id: int) -> Student:
        return self._students.get(student_id)

    def save(self, student: Student) -> None:
        self._students[student.student_id] = student # suprascrie daca exista deja

    def remove(self, student_id: int) -> bool:
        if student_id not in self._students:
            return False
        self._students.pop(student_id)
        return True

    def find_by_name(self, name: str) -> list[Student]:
        result = []
        for student in self._students.items():
            if name.lower() in student[1].name.lower():
                result.append(student[1])
        return result


