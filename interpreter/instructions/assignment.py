from interpreter.interfaces.instruction import Instruction


class Assignment(Instruction):
    def __init__(self, line, column, name, expression):
        self.line = line
        self.column = column
        self.name = name
        self.expression = expression

    def execute(self, syntax_tree, environment):
        symbol = self.expression.execute(syntax_tree, environment)  # Se obtiene el símbolo de la expresión.

        environment.set_variable(syntax_tree, self.name, symbol)  # Se edita el símbolo en el entorno.
