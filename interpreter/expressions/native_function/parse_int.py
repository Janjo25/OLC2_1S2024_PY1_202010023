from interpreter.environment.symbol import Symbol
from interpreter.environment.types import Types
from interpreter.interfaces.expression import Expression


class ParseInt(Expression):
    def __init__(self, line, column, expression):
        self.line = line
        self.column = column
        self.expression = expression

    def execute(self, syntax_tree, environment):
        result = self.expression.execute(syntax_tree, environment)

        if result.kind == Types.STRING:
            float_value = float(result.value)  # Se debe convertir el valor a flotante para poder convertirlo a entero.
            parsed_value = int(float_value)  # Se intenta convertir el valor a entero.

            return Symbol(self.line, self.column, parsed_value, Types.NUMBER)
        else:
            error_description = "no fue posible convertir el valor a int"

            syntax_tree.set_errors(self.line, self.column, error_description, environment.name, "semántico")

            return Symbol(self.line, self.column, None, Types.NULL)
