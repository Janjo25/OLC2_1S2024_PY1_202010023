from interpreter.environment.types import Types
from interpreter.interfaces.instruction import Instruction


class ArrayDeclaration(Instruction):
    def __init__(self, line, column, name, kind, expression):
        self.line = line
        self.column = column
        self.name = name
        self.kind = kind
        self.expression = expression

    def execute(self, syntax_tree, environment):
        symbol = self.expression.execute(syntax_tree, environment)

        if symbol.kind != Types.ARRAY:
            error_description = f"se esperaba un arreglo en la declaración de '{self.name}'."

            syntax_tree.set_errors(self.line, self.column, error_description, environment.name, "semántico")

            return

        """Función recursiva para validar cada elemento de un arreglo potencialmente multidimensional."""

        def validate_array_elements(elements, expected_type):
            for element in elements:
                if isinstance(element, list):  # El elemento es otra dimensión de la matriz.
                    if not validate_array_elements(element, expected_type):
                        return False
                elif element.kind != expected_type:
                    return False

            return True

        if not validate_array_elements(symbol.value, self.kind):
            error_description = f"los elementos del arreglo '{self.name}' no son del tipo esperado."

            syntax_tree.set_errors(self.line, self.column, error_description, environment.name, "semántico")

            return

        environment.check_variable(syntax_tree, self.name, symbol)
