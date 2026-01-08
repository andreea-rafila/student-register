from srm.command.Command import Command
from srm.exceptions.CommandException import CommandException
from srm.model.Discipline import Discipline
from srm.model.Student import Student
from srm.service.Service import Service


class UpdateCommand(Command):
    def __init__(self, entity, new_name: str, service: Service):
        self.entity = entity
        self.new_name = new_name
        self.service = service

    def undo(self) -> None:
        if isinstance(self.entity, Student):
            self.service.update_student(student_id=self.entity.student_id, new_name=self.entity.name)
        elif isinstance(self.entity, Discipline):
            self.service.update_discipline(discipline_id=self.entity.discipline_id, new_name=self.entity.name)
        else:
            raise CommandException("Unsupported entity type for UpdateCommand")

    def execute(self) -> None:
        if isinstance(self.entity, Student):
            self.service.update_student(student_id=self.entity.student_id, new_name=self.new_name)
        elif isinstance(self.entity, Discipline):
            self.service.update_discipline(discipline_id=self.entity.discipline_id, new_name=self.new_name)
        else:
            raise CommandException("Unsupported entity type for UpdateCommand")

    def __str__(self) -> str:
        return "UpdateCommand: " + repr(self.entity)

    def __repr__(self) -> str:
        return self.__str__()
