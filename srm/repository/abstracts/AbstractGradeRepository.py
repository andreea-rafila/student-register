from abc import ABC, abstractmethod

from srm.model.Grade import Grade


class AbstractGradeRepository(ABC):
    @abstractmethod
    def find_all(self) -> list[Grade]:
        pass

    @abstractmethod
    def save(self, grade: Grade) -> None:
        pass

    @abstractmethod
    def find_by_student(self, student_id: int) -> list[Grade]:
        pass

    @abstractmethod
    def find_by_discipline(self, discipline_id: int) -> list[Grade]:
        pass

    @abstractmethod
    def remove_by_student(self, student_id:int) -> list[Grade]:
        pass

    @abstractmethod
    def remove_by_discipline(self, discipline_id:int) -> list[Grade]:
        pass

    @abstractmethod
    def remove_grade(self, student_id:int, discipline_id:int, grade_value: int) -> bool:
        pass


