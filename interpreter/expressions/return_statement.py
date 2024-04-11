from interpreter.environment.symbol import Symbol
from interpreter.environment.types import Types


class ReturnStatement:
    def __init__(self, line, column, expression):
        self.line = line
        self.column = column
        self.expression = expression

    def execute(self, syntax_tree, environment):
        if environment.is_within_function():
            if self.expression is None:  # Si es un return sin valor, se retorna un valor nulo.
                return Symbol(self.line, self.column, None, Types.RETURN)

            symbol = self.expression.execute(syntax_tree, environment)

            return Symbol(self.line, self.column, symbol, Types.RETURN)

        error_description = "sentencia de transferencia fuera de una estructura de control"

        syntax_tree.set_errors(self.line, self.column, error_description, environment.name, "semántico")

        return Symbol(self.line, self.column, None, Types.NULL)
