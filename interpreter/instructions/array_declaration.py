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

        if symbol.kind != Types.ARRAY:  # Se verifica que el tipo del símbolo retornado sea un arreglo.
            error_description = f"el tipo de dato '{self.kind}' no coincide con el tipo del arreglo"

            syntax_tree.set_errors(self.line, self.column, error_description, environment.name, "semántico")

            return

        for value in symbol.value:  # Se recorre el arreglo que contiene el símbolo retornado.
            if value.kind != self.kind:  # Se revisa cada valor del arreglo para verificar que sea del tipo correcto.
                error_description = f"el tipo de dato '{self.name}' no coincide con el tipo del arreglo"

                syntax_tree.set_errors(self.line, self.column, error_description, environment.name, "semántico")

                return

        environment.check_variable(syntax_tree, self.name, symbol)
