from interpreter.interfaces.instruction import Instruction


class InterfaceAssignment(Instruction):
    def __init__(self, line, column, name, expression):
        self.line = line
        self.column = column
        self.name = name
        self.expression = expression  # Expresión que representa el valor a asignar.

    def execute(self, syntax_tree, environment):
        symbol = self.expression.execute(syntax_tree, environment)  # Se obtiene el símbolo de la expresión.

        chained_name = ".".join(self.name)

        environment.set_interface(syntax_tree, chained_name, symbol)  # Se edita el símbolo en el entorno.
