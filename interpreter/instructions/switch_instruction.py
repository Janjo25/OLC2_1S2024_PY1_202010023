from interpreter.environment.environment import Environment
from interpreter.environment.execute import instructions_executor
from interpreter.environment.symbol import Symbol
from interpreter.environment.types import Types
from interpreter.interfaces.instruction import Instruction


class SwitchInstruction(Instruction):
    def __init__(self, line, column, expression, cases, default_case=None):
        self.line = line
        self.column = column
        self.expression = expression
        self.cases = cases
        self.default_case = default_case

    """Este método ejecuta las instrucciones de un bloque 'switch'. Para lograrlo, se hace lo siguiente:
       1. Se evalúa la condición del 'switch' para obtener su valor.
       2. Se recorren la tupla de casos, que contiene la condición y las instrucciones de cada caso.
       3. Si el valor de la condición es igual al valor de la condición del caso, se ejecutan sus instrucciones.
          Si no se usa la instrucción 'break', se ejecutarán todos los casos que sigan al caso actual.
       4. Si el valor de la condición no es igual al valor de la condición del caso, se sigue recorriendo la tupla.
       5. Si no se encuentra coincidencia con el valor de la condición, se ejecutan las instrucciones por defecto."""

    def execute(self, syntax_tree, environment):
        condition_value = self.expression.execute(syntax_tree, environment).value

        found_matching_case = False  # Si es verdadero, se ejecutarán los casos que sigan al caso actual.

        for case_expression, case_instructions in self.cases:
            if found_matching_case or condition_value == case_expression.execute(syntax_tree, environment).value:
                found_matching_case = True

                case_environment = Environment(environment, "case")

                result = instructions_executor(case_instructions, syntax_tree, case_environment)

                if isinstance(result, Symbol):
                    if result.kind == Types.BREAK:
                        break

        if not found_matching_case and self.default_case is not None:
            default_environment = Environment(environment, "default")

            instructions_executor(self.default_case, syntax_tree, default_environment)
