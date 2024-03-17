from interpreter.environment.environment import Environment
from interpreter.environment.execute import instructions_executor
from interpreter.interfaces.instruction import Instruction


class IfInstruction(Instruction):
    def __init__(self, line, column, expression, true_instructions, false_instructions=None):
        self.line = line
        self.column = column
        self.expression = expression
        self.true_instructions = true_instructions
        self.false_instructions = false_instructions

    """Este método ejecuta las instrucciones de un bloque 'if', 'else if' o 'else'. Para lograrlo, se hace lo siguiente:
       1. Se evalúa la condición del bloque.
       2. Si la condición es verdadera, se ejecutan las instrucciones del bloque 'if'.
       3. Si la condición es falsa, se revisa si las instrucciones del bloque son una instancia de 'IfInstruction'.
          Si son una instancia, se vuelve a ejecutar el método 'execute' con las nuevas instrucciones.
          En esta nueva ejecución, se repite el mismo proceso.
          Si no son una instancia, se ejecutan las instrucciones del bloque 'else'."""

    def execute(self, syntax_tree, environment):
        condition = self.expression.execute(syntax_tree, environment)

        if condition.value is True:
            new_environment = Environment(environment, "if")

            return_value = instructions_executor(self.true_instructions, syntax_tree, new_environment)
        else:
            if isinstance(self.false_instructions, IfInstruction):
                return_value = self.false_instructions.execute(syntax_tree, environment)
            else:
                new_environment = Environment(environment, "else")

                return_value = instructions_executor(self.false_instructions, syntax_tree, new_environment)

        if return_value is not None:
            return return_value

        return None
