from srm.command.AddCommand import AddCommand
from srm.command.RemoveCommand import RemoveCommand
from srm.command.UpdateCommand import UpdateCommand
from srm.command.CommandHistory import CommandHistory
from srm.model.Student import Student
from srm.model.Discipline import Discipline
from srm.model.Grade import Grade
from srm.service.Service import Service
from srm.exceptions.NotFoundException import NotFoundException
from srm.exceptions.ValidationException import ValidationException


class ConsoleUI:
    def __init__(self, service: Service, history: CommandHistory):
        self._service = service
        self._history = history
        self._running = True

    @staticmethod
    def _read_int(prompt: str) -> int:
        s = input(prompt).strip()
        return int(s)

    @staticmethod
    def _read_str(prompt: str) -> str:
        return input(prompt).strip()

    @staticmethod
    def _print_list(title: str, items: list) -> None:
        print(f"\n{title}")
        if not items:
            print("(empty)")
            return
        for x in items:
            print(x)

    # Main loop
    def run(self) -> None:
        while self._running:
            self._print_main_menu()
            cmd = input("Choose option: ").strip().lower()

            try:
                if cmd == "1":
                    self._students_menu()
                elif cmd == "2":
                    self._disciplines_menu()
                elif cmd == "3":
                    self._grades_menu()
                elif cmd == "4":
                    self._search_menu()
                elif cmd == "5":
                    self._statistics_menu()
                elif cmd == "u":
                    self._do_undo()
                elif cmd == "r":
                    self._do_redo()
                elif cmd == "0":
                    self._running = False
                else:
                    print("Invalid option.")

            except (NotFoundException, ValidationException) as e:
                print(f"Input error: {e}")
            except ValueError:
                print("Invalid number input.")
            except Exception as e:
                print(f"Error: {e}")

    @staticmethod
    def _print_main_menu() -> None:
        print("\n==================== SRM MENU ====================")
        print("1. Manage students")
        print("2. Manage disciplines")
        print("3. Grade operations")
        print("4. Search")
        print("5. Statistics")
        print("U. Undo")
        print("R. Redo")
        print("0. Exit")
        print("==================================================")

    def _do_undo(self) -> None:
        if self._history.current_index < 0:
            print("Nothing to undo.")
            return
        self._history.undo()
        print("Undo done.")

    def _do_redo(self) -> None:
        if self._history.current_index >= len(self._history.history) - 1:
            print("Nothing to redo.")
            return
        self._history.redo()
        print("Redo done.")

    # Students
    def _students_menu(self) -> None:
        while True:
            print("\n--- Students ---")
            print("1. Add student")
            print("2. Remove student")
            print("3. Update student")
            print("4. List students")
            print("0. Back")

            cmd = input("Choose option: ").strip()

            if cmd == "1":
                student_id = self._read_int("Student id: ")
                name = self._read_str("Name: ")
                self._history.add_command(AddCommand(Student(student_id, name), self._service))
                print("Student added.")

            elif cmd == "2":
                student_id = self._read_int("Student id to remove: ")
                student = self._service.get_student_by_id(student_id)
                if student is None:
                    print("No such student.")
                    continue
                self._history.add_command(RemoveCommand(student, self._service))
                print("Student removed.")

            elif cmd == "3":
                student_id = self._read_int("Student id to update: ")
                student = self._service.get_student_by_id(student_id)
                if student is None:
                    print("No such student.")
                    continue
                new_name = self._read_str("New name: ")
                self._history.add_command(UpdateCommand(student, new_name, self._service))
                print("Student updated.")

            elif cmd == "4":
                self._print_list("All students:", self._service.student_repo.find_all())

            elif cmd == "0":
                return
            else:
                print("Invalid option.")

    # Disciplines
    def _disciplines_menu(self) -> None:
        while True:
            print("\n--- Disciplines ---")
            print("1. Add discipline")
            print("2. Remove discipline")
            print("3. Update discipline")
            print("4. List disciplines")
            print("0. Back")

            cmd = input("Choose option: ").strip()

            if cmd == "1":
                discipline_id = self._read_int("Discipline id: ")
                name = self._read_str("Name: ")
                self._history.add_command(AddCommand(Discipline(discipline_id, name), self._service))
                print("Discipline added.")

            elif cmd == "2":
                discipline_id = self._read_int("Discipline id to remove: ")
                discipline = self._service.get_discipline_by_id(discipline_id)
                if discipline is None:
                    print("No such discipline.")
                    continue
                self._history.add_command(RemoveCommand(discipline, self._service))
                print("Discipline removed.")

            elif cmd == "3":
                discipline_id = self._read_int("Discipline id to update: ")
                discipline = self._service.get_discipline_by_id(discipline_id)
                if discipline is None:
                    print("No such discipline.")
                    continue
                new_name = self._read_str("New name: ")
                self._history.add_command(UpdateCommand(discipline, new_name, self._service))
                print("Discipline updated.")

            elif cmd == "4":
                self._print_list("All disciplines:", self._service.discipline_repo.find_all())

            elif cmd == "0":
                return
            else:
                print("Invalid option.")

    # Grades
    def _grades_menu(self) -> None:
        while True:
            print("\n--- Grades ---")
            print("1. Add grade")
            print("2. Remove grade (exact match)")
            print("3. List all grades")
            print("4. List grades by student")
            print("5. List grades by discipline")
            print("0. Back")

            cmd = input("Choose option: ").strip()

            if cmd == "1":
                student_id = self._read_int("Student id: ")
                discipline_id = self._read_int("Discipline id: ")
                grade_value = self._read_int("Grade value: ")

                if self._service.get_student_by_id(student_id) is None:
                    print("No such student.")
                    continue
                if self._service.get_discipline_by_id(discipline_id) is None:
                    print("No such discipline.")
                    continue

                self._history.add_command(AddCommand(Grade(student_id, discipline_id, grade_value), self._service))
                print("Grade added.")

            elif cmd == "2":
                student_id = self._read_int("Student id: ")
                discipline_id = self._read_int("Discipline id: ")
                grade_value = self._read_int("Grade value: ")

                self._history.add_command(RemoveCommand(Grade(student_id, discipline_id, grade_value), self._service))
                print("Grade removed (if it existed).")

            elif cmd == "3":
                self._print_list("All grades:", self._service.get_all_grades())

            elif cmd == "4":
                student_id = self._read_int("Student id: ")
                self._print_list(
                    f"Grades for student {student_id}:",
                    self._service.get_grades_by_student(student_id)
                )

            elif cmd == "5":
                discipline_id = self._read_int("Discipline id: ")
                self._print_list(
                    f"Grades for discipline {discipline_id}:",
                    self._service.get_grades_by_discipline(discipline_id)
                )

            elif cmd == "0":
                return
            else:
                print("Invalid option.")

    # Search
    def _search_menu(self) -> None:
        while True:
            print("\n--- Search ---")
            print("1. Search students (id or name substring)")
            print("2. Search disciplines (id or name substring)")
            print("0. Back")

            cmd = input("Choose option: ").strip()

            if cmd == "1":
                q = self._read_str("Search query: ")
                if q.isdigit():
                    student = self._service.get_student_by_id(int(q))
                    if student is None:
                        print("No match.")
                    else:
                        print(student)
                else:
                    results = self._service.get_students_by_name(q)
                    self._print_list("Matches:", results)

            elif cmd == "2":
                q = self._read_str("Search query: ")
                if q.isdigit():
                    d = self._service.get_discipline_by_id(int(q))
                    if d is None:
                        print("No match.")
                    else:
                        print(d)
                else:
                    results = self._service.get_disciplines_by_name(q)
                    self._print_list("Matches:", results)

            elif cmd == "0":
                return
            else:
                print("Invalid option.")

    # Statistics
    def _statistics_menu(self) -> None:
        while True:
            print("\n--- Statistics ---")
            print("1. All students failing at one or more disciplines")
            print("2. Students with best situation (aggregate avg desc)")
            print("3. Disciplines with grades (avg desc)")
            print("0. Back")

            cmd = input("Choose option: ").strip()

            if cmd == "1":
                self._print_list("Failing students:", self._service.stat_1())

            elif cmd == "2":
                print("\nStudent situations (descending):")
                stats = self._service.stat_2()
                if not stats:
                    print("(empty)")
                else:
                    for student, avg in stats.items():
                        print(f"{student} -> {avg:.2f}")

            elif cmd == "3":
                print("\nDiscipline averages (descending):")
                stats = self._service.stat_3()
                if not stats:
                    print("(empty)")
                else:
                    for discipline, avg in stats.items():
                        print(f"{discipline} -> {avg:.2f}")

            elif cmd == "0":
                return
            else:
                print("Invalid option.")



