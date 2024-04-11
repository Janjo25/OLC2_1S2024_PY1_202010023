from interpreter.environment.symbol import Symbol
from interpreter.environment.types import Types
from interpreter.interfaces.instruction import Instruction


class Array(Instruction):
    def __init__(self, line, column, expressions=None):
        self.line = line
        self.column = column

        if expressions is None:
            expressions = []

        self.expressions = expressions

    def execute(self, syntax_tree, environment):
        """Función para procesar recursivamente una expresión que puede ser una lista de expresiones."""

        def process_expression(expression):
            if isinstance(expression, list):
                return [process_expression(subexpression) for subexpression in expression]
            else:
                return expression.execute(syntax_tree, environment)

        array_values = [process_expression(expression) for expression in self.expressions]

        return Symbol(self.line, self.column, array_values, Types.ARRAY)
