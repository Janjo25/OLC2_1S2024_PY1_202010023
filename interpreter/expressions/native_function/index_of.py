from interpreter.environment.symbol import Symbol
from interpreter.environment.types import Types
from interpreter.interfaces.expression import Expression


class IndexOf(Expression):
    def __init__(self, line, column, array, expression):
        self.line = line
        self.column = column
        self.array = array
        self.expression = expression

    def execute(self, syntax_tree, environment):
        result = self.array.execute(syntax_tree, environment)

        if result.kind == Types.ARRAY:
            search_value = self.expression.execute(syntax_tree, environment).value

            for index, element in enumerate(result.value):  # Se busca el valor en el arreglo.
                if element.value == search_value:  # Si se encuentra el valor, se retorna el índice.
                    return Symbol(self.line, self.column, index, Types.NUMBER)
        else:
            error_description = "la función 'indexOf' solo puede ser aplicada a arreglos"

            syntax_tree.set_errors(self.line, self.column, error_description, environment.name, "semántico")

            return Symbol(self.line, self.column, None, Types.NULL)

        return Symbol(self.line, self.column, -1, Types.NUMBER)
