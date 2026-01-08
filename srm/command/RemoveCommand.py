from srm.command.Command import Command
from srm.exceptions.CommandException import CommandException
from srm.model.Discipline import Discipline
from srm.model.Grade import Grade
from srm.model.Student import Student
from srm.service.Service import Service


class RemoveCommand(Command):
    def __init__(self, entity, service: Service):
        # pentru student -id name, trebuie doar id pt remove
        # pentru disciplina - id name, trebuie doar id pt remove
        # pentru grade - student_id, discipline_id, grade_value

        self.entity = entity # aici ramane obiectul student
        self.service = service
        self.was_removed = None
        self.grade_backup = None  # doar daca e cazul

    def undo(self) -> None:
        if isinstance(self.entity, Student):
            if self.was_removed:
                self.service.add_student(student_id=self.entity.student_id, name=self.entity.name)
                for grade in self.grade_backup:
                    self.service.add_grade(student_id=grade.student_id, discipline_id=grade.discipline_id,
                                           grade_value=grade.grade_value)
        elif isinstance(self.entity, Discipline):
            if self.was_removed:
                self.service.add_discipline(discipline_id=self.entity.discipline_id, name=self.entity.name)
                for grade in self.grade_backup:
                    self.service.add_grade(student_id=grade.student_id, discipline_id=grade.discipline_id,
                                           grade_value=grade.grade_value)
        elif isinstance(self.entity, Grade):
            if self.was_removed:
                self.service.add_grade(student_id=self.entity.student_id, discipline_id=self.entity.discipline_id,
                                   grade_value=self.entity.grade_value)
        else:
            raise CommandException("Unsupported entity type for RemoveCommand")

    def execute(self) -> None:
        if isinstance(self.entity, Student):
            self.was_removed, self.grade_backup = self.service.remove_student(student_id=self.entity.student_id) # de aici primesti tuple [bool, list[Grade]]
            # self.was_removed = bool
            # self.grade_backup = list[Grade]
        elif isinstance(self.entity, Discipline):
            self.was_removed, self.grade_backup = self.service.remove_discipline(discipline_id=self.entity.discipline_id)
        elif isinstance(self.entity, Grade):
            self.was_removed = self.service.remove_grade(student_id=self.entity.student_id, discipline_id=self.entity.discipline_id, grade_value=self.entity.grade_value)
        else:
            raise CommandException("Unsupported entity type for RemoveCommand")

    def __str__(self) -> str:
        return "RemoveCommand: " + repr(self.entity)

    def __repr__(self) -> str:
        return self.__str__()