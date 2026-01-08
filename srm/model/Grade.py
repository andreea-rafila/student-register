class Grade:
    def __init__(self, student_id: int, discipline_id: int, grade_value: int):
        self.student_id = student_id
        self.discipline_id = discipline_id
        self.grade_value = grade_value

    def __str__(self) -> str:
        return f"Grade(Student ID: {self.student_id}, Discipline ID: {self.discipline_id}, Grade: {self.grade_value})"

    def __repr__(self) -> str:
        return self.__str__()