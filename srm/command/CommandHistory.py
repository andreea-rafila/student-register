from srm.command.Command import Command


class CommandHistory:
    def __init__(self):
        self.history = []
        self.current_index = -1

    def add_command(self, command: Command):
        # If we are not at the end of the history, truncate the future commands
        if self.current_index < len(self.history) - 1:
            self.history = self.history[:self.current_index + 1]
        self.history.append(command)
        command.execute()
        self.current_index += 1

    def undo(self) -> None:
        if self.current_index >= 0:
            self.history[self.current_index].undo()
            self.current_index -= 1

    def redo(self) -> None:
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            self.history[self.current_index].execute()

    def clear_history(self):
        self.history = []
        self.current_index = -1

    def get_current_state(self) -> list[Command]:
        return self.history

