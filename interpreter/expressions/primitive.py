from interpreter.environment.symbol import Symbol
from interpreter.interfaces.expression import Expression


class Primitive(Expression):
    def __init__(self, line, column, value, kind):
        self.line = line
        self.column = column
        self.value = value
        self.kind = kind

    def execute(self, syntax_tree, environment):
        return Symbol(self.line, self.column, self.value, self.kind)
