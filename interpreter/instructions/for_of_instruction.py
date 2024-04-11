from interpreter.environment.environment import Environment
from interpreter.environment.execute import instructions_executor
from interpreter.environment.symbol import Symbol
from interpreter.environment.types import Types
from interpreter.interfaces.instruction import Instruction


class ForOfInstruction(Instruction):
    def __init__(self, line, column, variable_name, iterable_expression, instructions):
        self.line = line
        self.column = column
        self.variable_name = variable_name  # Nombre de la variable que contendrá el valor actual del iterable.
        self.iterable_expression = iterable_expression  # Expresión que se recorrerá con el ciclo.
        self.instructions = instructions  # Instrucciones que se ejecutarán en cada iteración del ciclo.

    def execute(self, syntax_tree, environment):
        iterable_symbol = self.iterable_expression.execute(syntax_tree, environment)

        if len(iterable_symbol.value) == 0:  # Se revisa que el iterable no esté vacío.
            return None  # Ya que no hay elementos en el iterable, no se ejecuta el ciclo.

        variable_kind = iterable_symbol.value[0].kind  # Se obtiene el tipo del primer elemento del iterable.
        variable_symbol = Symbol(self.line, self.column, None, variable_kind)  # Estado inicial de la variable.

        loop_environment = Environment(environment, "for-of")  # Se crea un nuevo ambiente para el ciclo.
        loop_environment.check_variable(syntax_tree, self.variable_name, variable_symbol)

        if not isinstance(iterable_symbol.value, list):  # Se revisa que el iterable sea una lista.
            error_description = "el ciclo 'for-of' solo puede recorrer listas"

            syntax_tree.set_errors(self.line, self.column, error_description, environment.name, "semántico")

            return Symbol(self.line, self.column, None, Types.NULL)

        for element in iterable_symbol.value:  # Se itera sobre los elementos del iterable.
            variable_symbol = Symbol(self.line, self.column, element.value, element.kind)  # Se actualiza el símbolo.
            loop_environment.set_variable(syntax_tree, self.variable_name, variable_symbol)

            result = instructions_executor(self.instructions, syntax_tree, loop_environment)

            if isinstance(result, Symbol):
                if result.kind == Types.BREAK:
                    break
                if result.kind == Types.CONTINUE:
                    continue
                if result.kind == Types.RETURN:
                    return result
