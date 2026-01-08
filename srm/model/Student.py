class Student:
    def __init__(self, student_id: int, name: str):
        self.student_id = student_id
        self.name = name

    def __str__(self) -> str:
        return f"Student(ID: {self.student_id}, Name: {self.name})"

    def __repr__(self) -> str:
        return self.__str__()
