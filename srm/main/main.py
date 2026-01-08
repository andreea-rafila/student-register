import os

from srm.command.CommandHistory import CommandHistory
from srm.exceptions.SettingsException import SettingsException
from srm.repository.binary.BinaryDisciplineRepository import BinaryDisciplineRepository
from srm.repository.binary.BinaryGradeRepository import BinaryGradeRepository
from srm.repository.binary.BinaryStudentRepository import BinaryStudentRepository
from srm.repository.file.FileDisciplineRepository import FileDisciplineRepository
from srm.repository.file.FileGradeRepository import FileGradeRepository
from srm.repository.file.FileStudentRepository import FileStudentRepository
from srm.repository.in_memory.DisciplineRepository import DisciplineRepository
from srm.repository.in_memory.GradeRepository import GradeRepository
from srm.repository.in_memory.StudentRepository import StudentRepository
from srm.service.Service import Service
from srm.settings.Settings import Settings
from srm.ui.ConsoleUI import ConsoleUI
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



def _default_settings_path() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(os.path.dirname(here), "settings", "settings.properties")


def main():
    settings_path = _default_settings_path()

    try:
        settings = Settings(settings_path)
    except SettingsException as e:
        print("SettingsException caught:", e)
        return

    if settings.repository == "inmemory":
        student_repo = StudentRepository()
        discipline_repo = DisciplineRepository()
        grade_repo = GradeRepository()
    elif settings.repository == "textfiles":
        student_repo = FileStudentRepository(settings.students_path)
        discipline_repo = FileDisciplineRepository(settings.disciplines_path)
        grade_repo = FileGradeRepository(settings.grades_path)
    elif settings.repository == "binaryfiles":
        student_repo = BinaryStudentRepository(settings.students_path)
        discipline_repo = BinaryDisciplineRepository(settings.disciplines_path)
        grade_repo = BinaryGradeRepository(settings.grades_path)
    else:
        print("Invalid settings.repository (use: inmemory / textfiles / binaryfiles)")
        return

    service = Service(
        student_repo=student_repo,
        discipline_repo=discipline_repo,
        grade_repo=grade_repo
    )

    # at least 20 generated items at startup.
    # If repos are empty, populate.
    if len(service.student_repo.find_all()) < 20 or len(service.discipline_repo.find_all()) < 20:
        service.populate_example_data()

    history = CommandHistory()
    ui = ConsoleUI(service, history)
    ui.run()


if __name__ == "__main__":
    main()

