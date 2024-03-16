from interpreter.environment.error import Error


class SyntaxTree:
    def __init__(self):
        self.console = ""
        self.errors = []
        self.instructions = []

    def set_console(self, text):
        self.console += text + "\n"

    def get_console(self):
        return self.console

    def set_errors(self, line, column, description, scope, kind):
        error = Error(line, column, description, scope, kind)

        self.errors.append(error)

    def get_errors(self):
        return self.errors

    def set_instructions(self, instruction):
        self.instructions += instruction

    def get_instructions(self):
        return self.instructions
