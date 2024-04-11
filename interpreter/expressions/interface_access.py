from interpreter.environment.symbol import Symbol
from interpreter.interfaces.expression import Expression


class InterfaceAccess(Expression):
    def __init__(self, line, column, expression, field_chain):
        self.line = line
        self.column = column
        self.expression = expression  # Expresión que evalúa la instancia inicial de la interfaz.
        self.field_chain = field_chain  # Lista de nombres que representan la cadena de acceso.

    def execute(self, syntax_tree, environment):
        current_symbol = self.expression.execute(syntax_tree, environment)

        for field_name in self.field_chain:  # Se recorre la cadena de acceso para acceder a los campos anidados.
            if not isinstance(current_symbol.value, dict):
                error_description = f"se intentó acceder a un campo en una instancia que no es de tipo 'interface'"

                syntax_tree.set_errors(self.line, self.column, error_description, environment.name, "semántico")

                return None

            if field_name not in current_symbol.value:  # Se verifica si el campo existe en la instancia actual.
                error_description = f"el campo '{field_name}' no existe en la instancia de la interfaz"

                syntax_tree.set_errors(self.line, self.column, error_description, environment.name, "semántico")

                return None

            current_symbol = current_symbol.value[field_name]  # Se accede al siguiente nivel en la cadena de acceso.

        return Symbol(self.line, self.column, current_symbol.value, current_symbol.kind)
