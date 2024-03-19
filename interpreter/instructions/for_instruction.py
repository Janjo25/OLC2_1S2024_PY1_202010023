from interpreter.environment.environment import Environment
from interpreter.environment.execute import instructions_executor
from interpreter.environment.symbol import Symbol
from interpreter.environment.types import Types
from interpreter.interfaces.instruction import Instruction


class ForInstruction(Instruction):
    def __init__(self, line, column, initialization, condition, update, instructions):
        self.line = line
        self.column = column
        self.initialization = initialization  # Almacena la inicialización de la variable de control.
        self.condition = condition  # Almacena la condición de control.
        self.update = update  # Almacena la actualización de la variable de control.
        self.instructions = instructions  # Almacena las instrucciones a ejecutar.

    def execute(self, syntax_tree, environment):
        self.initialization.execute(syntax_tree, environment)

        while self.condition.execute(syntax_tree, environment).value:
            loop_environment = Environment(environment, "for")

            result = instructions_executor(self.instructions, syntax_tree, loop_environment)

            self.update.execute(syntax_tree, environment)  # Se debe de actualizar la variable de control.

            if isinstance(result, Symbol):
                if result.kind == Types.BREAK:
                    break
