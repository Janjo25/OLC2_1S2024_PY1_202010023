from interpreter.environment.symbol import Symbol
from interpreter.environment.types import Types
from interpreter.interfaces.expression import Expression


class Typeof(Expression):
    def __init__(self, line, column, expression):
        self.line = line
        self.column = column
        self.expression = expression

    def execute(self, syntax_tree, environment):
        result = self.expression.execute(syntax_tree, environment)

        if result.kind == Types.NUMBER:
            return Symbol(self.line, self.column, "number", Types.STRING)
        elif result.kind == Types.FLOAT:
            return Symbol(self.line, self.column, "float", Types.STRING)
        elif result.kind == Types.STRING:
            return Symbol(self.line, self.column, "string", Types.STRING)
        elif result.kind == Types.BOOLEAN:
            return Symbol(self.line, self.column, "boolean", Types.STRING)
        elif result.kind == Types.CHAR:
            return Symbol(self.line, self.column, "char", Types.STRING)
        elif result.kind == Types.ARRAY:
            return Symbol(self.line, self.column, "array", Types.STRING)
        elif result.kind == Types.INTERFACE:
            return Symbol(self.line, self.column, "interface", Types.STRING)
