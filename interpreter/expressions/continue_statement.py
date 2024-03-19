from interpreter.environment.symbol import Symbol
from interpreter.environment.types import Types
from interpreter.interfaces.expression import Expression


class ContinueStatement(Expression):
    def __init__(self, line, column):
        self.line = line
        self.column = column

    def execute(self, syntax_tree, environment):
        if environment.is_within_control_flow():
            return Symbol(self.line, self.column, None, Types.CONTINUE)

        error_description = "sentencia de transferencia fuera de una estructura de control"

        syntax_tree.set_errors(self.line, self.column, error_description, environment.name, "semántico")

        return Symbol(self.line, self.column, None, Types.NULL)
