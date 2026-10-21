# Student Register

A console application in Python for managing students, disciplines and grades, built on a layered architecture with **unlimited undo/redo** and **interchangeable storage back ends**.

```
=================== SRM MENU ===================
1. Manage students
2. Manage disciplines
3. Grade operations
4. Search
5. Statistics
U. Undo
R. Redo
0. Exit
================================================
```

## Features
- Add, remove, update and search students, disciplines and grades
- **Unlimited undo/redo** using the Command design pattern, with cascading operations: removing a student also removes their grades, and undoing it restores everything
- **Three storage back ends**: in-memory, text file (JSON) and binary file, chosen in `settings.properties` without changing any code
- Statistics:
  - students failing at least one discipline
  - students ranked by their aggregated average
  - disciplines ranked by the average grade received
- Input validation with custom exceptions
- Unit tests for the service layer

## Architecture
```
srm/
├── model/        # Student, Discipline, Grade
├── repository/   # abstract repositories + in-memory, file and binary implementations
├── service/      # business logic and statistics
├── command/      # Command pattern: add/remove/update commands, undo/redo history
├── ui/           # console user interface
├── settings/     # reads settings.properties
├── exceptions/   # custom exceptions
└── tests/        # unit tests
```

## How to run
Requires Python 3.10+, no external libraries.

```bash
python -m srm.main.main
```

To change the storage type, edit `srm/settings/settings.properties`.

## Running the tests
```bash
python -m unittest discover
```
