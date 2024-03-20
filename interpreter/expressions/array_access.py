from interpreter.environment.types import Types
from interpreter.interfaces.expression import Expression


class ArrayAccess(Expression):
    def __init__(self, line, column, array, index):
        self.line = line
        self.column = column
        self.array = array
        self.index = index

    def execute(self, syntax_tree, environment):
        symbol = self.array.execute(syntax_tree, environment)

        if symbol.kind != Types.ARRAY:  # Se verifica que el tipo del símbolo retornado sea un arreglo.
            error_description = f"el tipo de dato '{self.array}' no coincide con el tipo del arreglo"

            syntax_tree.set_errors(self.line, self.column, error_description, environment.name, "semántico")

            return

        index = self.index.execute(syntax_tree, environment)  # Se obtiene el símbolo del índice.

        if index.kind != Types.NUMBER:  # Se verifica  que el valor del índice sea un número entero.
            error_description = "el índice debe ser de tipo numérico"

            syntax_tree.set_errors(self.line, self.column, error_description, environment.name, "semántico")

            return

        return symbol.value[index.value]  # Se retorna el valor del arreglo en la posición indicada por el índice.
