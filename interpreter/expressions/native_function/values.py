from interpreter.environment.symbol import Symbol
from interpreter.environment.types import Types
from interpreter.interfaces.expression import Expression


class Values(Expression):
    def __init__(self, line, column, expression):
        self.line = line
        self.column = column
        self.expression = expression

    def execute(self, syntax_tree, environment):
        result = self.expression.execute(syntax_tree, environment)

        if result.kind == Types.INTERFACE:
            values = list(result.value.values())

            return Symbol(self.line, self.column, values, Types.ARRAY)
        else:
            raise Exception(f"tipo inválido '{result.kind}' para función 'values'.")
