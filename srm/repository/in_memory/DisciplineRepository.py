from srm.model.Discipline import Discipline
from srm.repository.abstracts.AbstractDisciplineRepository import AbstractDisciplineRepository


class DisciplineRepository(AbstractDisciplineRepository):
    def __init__(self):
        self._disciplines: dict[int, Discipline] = {}

    def find_all(self) -> list[Discipline]:
        return list(self._disciplines.values())

    def find_one(self, discipline_id: int) -> Discipline:
        return self._disciplines.get(discipline_id)

    def save(self, discipline: Discipline) -> None:
        self._disciplines[discipline.discipline_id] = discipline

    def remove(self, discipline_id: int) -> bool:
        if discipline_id not in self._disciplines:
            return False
        self._disciplines.pop(discipline_id)
        return True

    def find_by_name(self, name: str) -> list[Discipline]:
        result = []
        for discipline in self._disciplines.items():
            if name.lower() in discipline[1].name.lower():
                result.append(discipline[1])
        return result

