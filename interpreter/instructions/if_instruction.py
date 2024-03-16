from interpreter.environment.environment import Environment
from interpreter.environment.execute import instructions_executor
from interpreter.interfaces.instruction import Instruction


class IfInstruction(Instruction):
    def __init__(self, line, column, expression, instructions):
        self.line = line
        self.column = column
        self.expression = expression  # Expresión que se evalúa para saber si se ejecuta el bloque del 'if'.
        self.instructions = instructions  # Lista que contiene las instrucciones del bloque del 'if'.

    def execute(self, syntax_tree, environment):
        condition = self.expression.execute(syntax_tree, environment)

        if condition.value is True:
            new_environment = Environment(environment, "if")  # Se crea un nuevo entorno para el bloque del 'if'.
            return_value = instructions_executor(self.instructions, syntax_tree, new_environment)

            if return_value is not None:
                return return_value

        return None
