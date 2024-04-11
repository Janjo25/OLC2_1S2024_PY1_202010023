from interpreter.environment.symbol import Symbol
from interpreter.environment.types import Types
from interpreter.interfaces.instruction import Instruction


class InterfaceInstantiation(Instruction):
    def __init__(self, line, column, name, values):
        self.line = line
        self.column = column
        self.name = name  # Nombre de la interfaz.
        self.values = values  # Dicciónario de los campos de la interfaz y sus valores.

    def execute(self, syntax_tree, environment):
        interface = environment.get_interface(syntax_tree, self.name)

        if not interface:  # Si la definición de la interfaz es 'None' entonces la interfaz no está definida.
            error_description = f"la interfaz '{self.name}' no está definida"

            syntax_tree.set_errors(self.line, self.column, error_description, environment.name, "semántico")

            return Symbol(self.line, self.column, None, Types.NULL)

        instance = {}  # Diccionario que contendrá los valores de los campos de la interfaz.

        for field_name, field_type in interface.items():
            if field_name in self.values:
                result = self.values[field_name].execute(syntax_tree, environment)  # Se obtiene el símbolo.

                instance[field_name] = result  # Se agrega el resultado al diccionario de campos de la interfaz.
            else:
                error_description = f"el campo '{field_name}' de la interfaz '{self.name}' no está definido"

                syntax_tree.set_errors(self.line, self.column, error_description, environment.name, "semántico")

                return Symbol(self.line, self.column, None, Types.NULL)

        return Symbol(self.line, self.column, instance, Types.INTERFACE)
