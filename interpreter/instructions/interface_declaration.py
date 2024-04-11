from interpreter.interfaces.instruction import Instruction


class InterfaceDeclaration(Instruction):
    def __init__(self, line, column, name, fields):
        self.line = line
        self.column = column
        self.name = name
        self.fields = fields

    def execute(self, syntax_tree, environment):
        environment.check_interface(self.line, self.column, syntax_tree, self.name, self.fields)

        return None
