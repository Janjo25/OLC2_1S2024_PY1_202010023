from interpreter.environment.symbol import Symbol
from interpreter.environment.types import Types
from interpreter.interfaces.expression import Expression


class Pop(Expression):
    def __init__(self, line, column, array):
        self.line = line
        self.column = column
        self.array = array

    def execute(self, syntax_tree, environment):
        result = self.array.execute(syntax_tree, environment)

        if result.kind == Types.ARRAY:
            if len(result.value) != 0:
                return result.value.pop()

            error_description = "no se puede extraer un elemento de un arreglo vacío"

            syntax_tree.set_errors(self.line, self.column, error_description, environment.name, "semántico")

            return Symbol(self.line, self.column, None, Types.NULL)
        else:
            error_description = "la función 'pop' solo puede ser aplicada a arreglos"

            syntax_tree.set_errors(self.line, self.column, error_description, environment.name, "semántico")

            return Symbol(self.line, self.column, None, Types.NULL)
