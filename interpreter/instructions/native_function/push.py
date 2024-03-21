from interpreter.environment.symbol import Symbol
from interpreter.environment.types import Types
from interpreter.interfaces.expression import Expression


class Push(Expression):
    def __init__(self, line, column, array, expression):
        self.line = line
        self.column = column
        self.array = array
        self.expression = expression

    def execute(self, syntax_tree, environment):
        result = self.array.execute(syntax_tree, environment)

        if result.kind == Types.ARRAY:
            element = self.expression.execute(syntax_tree, environment)

            result.value.append(element)  # Se agrega el elemento al arreglo.

            return None
        else:
            error_description = "La función 'push' solo puede ser aplicada a arreglos"

            syntax_tree.set_errors(self.line, self.column, error_description, environment.name, "semántico")

            return Symbol(self.line, self.column, None, Types.NULL)
