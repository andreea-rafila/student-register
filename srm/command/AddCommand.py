from srm.command.Command import Command
from srm.exceptions.CommandException import CommandException
from srm.model.Discipline import Discipline
from srm.model.Grade import Grade
from srm.model.Student import Student
from srm.service.Service import Service


class AddCommand(Command):
    def __init__(self, entity, service: Service):
        self.entity = entity
        self.service = service

    def undo(self) -> None:
        if isinstance(self.entity, Student):
            self.service.remove_student(student_id=self.entity.student_id)
        elif isinstance(self.entity, Discipline):
            self.service.remove_discipline(discipline_id=self.entity.discipline_id)
        elif isinstance(self.entity, Grade):
            self.service.remove_grade(student_id=self.entity.student_id, discipline_id=self.entity.discipline_id,
                                   grade_value=self.entity.grade_value)
        else:
            raise CommandException("Unsupported entity type for AddCommand")

    def execute(self) -> None:
        if isinstance(self.entity, Student):
            self.service.add_student(student_id=self.entity.student_id, name=self.entity.name)
        elif isinstance(self.entity, Discipline):
            self.service.add_discipline(discipline_id=self.entity.discipline_id, name=self.entity.name)
        elif isinstance(self.entity, Grade):
            self.service.add_grade(student_id=self.entity.student_id, discipline_id=self.entity.discipline_id, grade_value=self.entity.grade_value)
        else:
            raise CommandException("Unsupported entity type for AddCommand")

    def __str__(self) -> str:
        return "AddCommand: " + repr(self.entity)

    def __repr__(self) -> str:
        return self.__str__()

