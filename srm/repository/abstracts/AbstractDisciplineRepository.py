from abc import abstractmethod, ABC

from srm.model.Discipline import Discipline


class AbstractDisciplineRepository(ABC):
    @abstractmethod
    def find_all(self) -> list[Discipline]:
        pass
    @abstractmethod
    def find_one(self, discipline_id: int) -> Discipline:
        pass
    @abstractmethod
    def save(self, discipline: Discipline) -> None:
        pass
    @abstractmethod
    def remove(self, discipline_id: int) -> bool:
        pass
    @abstractmethod
    def find_by_name(self, name: str) -> list[Discipline]:
        pass
