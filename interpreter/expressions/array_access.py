from interpreter.environment.types import Types
from interpreter.interfaces.expression import Expression


class ArrayAccess(Expression):
    def __init__(self, line, column, array, indices):
        self.line = line
        self.column = column
        self.array = array
        self.indices = indices if isinstance(indices, list) else [indices]  # Los índices deben de ser una lista.

    def execute(self, syntax_tree, environment):
        symbol = self.array.execute(syntax_tree, environment)

        if symbol.kind != Types.ARRAY:
            error_description = f"intento de acceso a un índice de un valor que no es un arreglo: {symbol.value}"

            syntax_tree.set_errors(self.line, self.column, error_description, environment.name, "semántico")

            return

        """Se debe de recorrer los índices para obtener el valor que se encuentra en la posición deseada."""

        current_value = symbol.value

        for index_expression in self.indices:
            index_symbol = index_expression.execute(syntax_tree, environment)

            if index_symbol.kind != Types.NUMBER:
                error_description = "los índices de un arreglo deben de ser números enteros"

                syntax_tree.set_errors(self.line, self.column, error_description, environment.name, "semántico")

                return

            index = index_symbol.value

            if not (0 <= index < len(current_value)):  # Se debe de verificar que el índice no esté fuera de rango.
                error_description = f"índice fuera de rango: {index}"

                syntax_tree.set_errors(self.line, self.column, error_description, environment.name, "semántico")

                return

            current_value = current_value[index]

        return current_value
