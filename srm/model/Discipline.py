class Discipline:
    def __init__(self, discipline_id: int, name: str):
        self.discipline_id = discipline_id
        self.name = name

    def __str__(self) -> str:
        return f"Discipline(ID: {self.discipline_id}, Name: {self.name})"

    def __repr__(self) -> str:
        return self.__str__()



