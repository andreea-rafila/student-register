import json
from pathlib import Path

from srm.model.Discipline import Discipline
from srm.repository.abstracts.AbstractDisciplineRepository import AbstractDisciplineRepository


class FileDisciplineRepository(AbstractDisciplineRepository):

    def __init__(self, file_path: str):
        self._file_path = Path(file_path)
        self._disciplines: dict[int, Discipline] = {}
        self._load_from_file()


    def find_all(self) -> list[Discipline]:
        return list(self._disciplines.values())

    def find_one(self, discipline_id: int) -> Discipline:
        return self._disciplines.get(discipline_id)

    def save(self, discipline: Discipline) -> None:
        self._disciplines[discipline.discipline_id] = discipline
        self._write_to_file()

    def remove(self, discipline_id: int) -> bool:
        if discipline_id not in self._disciplines:
            return False
        self._disciplines.pop(discipline_id)
        self._write_to_file()
        return True

    def _load_from_file(self) -> None:
        if not self._file_path.exists():
            return

        with self._file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        for item in data:
            discipline = Discipline(
                discipline_id=item["discipline_id"],
                name=item["name"]
            )
            self._disciplines[discipline.discipline_id] = discipline

    def _write_to_file(self) -> None:
        data = [
            {
                "discipline_id": discipline.discipline_id,
                "name": discipline.name
            }
            for discipline in self._disciplines.values()
        ]

        # srm/repository/file/discipline.json
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        with self._file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def find_by_name(self, name: str) -> list[Discipline]:
        result = []
        for discipline in self._disciplines.items():
            if name.lower() in discipline[1].name.lower():
                result.append(discipline[1])
        return result

