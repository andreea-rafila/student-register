from abc import abstractmethod, ABC

from srm.model.Student import Student


class AbstractStudentRepository(ABC):
    @abstractmethod
    def find_all(self) -> list[Student]:
        pass
    @abstractmethod
    def find_one(self, student_id: int) -> Student:
        pass
    @abstractmethod
    def save(self, student: Student) -> None:
        pass
    @abstractmethod
    def remove(self, student_id: int) -> bool:
        pass
    @abstractmethod
    def find_by_name(self, name: str) -> list[Student]:
        pass

