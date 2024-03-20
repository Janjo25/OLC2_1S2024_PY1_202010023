from interpreter.environment.symbol import Symbol
from interpreter.environment.types import Types
from interpreter.interfaces.instruction import Instruction


class Array(Instruction):
    def __init__(self, line, column, expressions=None):
        self.line = line
        self.column = column
        self.expressions = expressions

    def execute(self, syntax_tree, environment):
        array_values = []

        try:
            if self.expressions is not None:  # Si no hay expresiones, se retorna un arreglo vacío.
                for expression in self.expressions:  # Se ejecuta cada expresión que se encuentre en el arreglo.
                    index_expression = expression.execute(syntax_tree, environment)

                    array_values.append(index_expression)  # Se agrega el símbolo retornado al arreglo.
        except TypeError:
            error_description = "declaración de arreglo incorrecta"

            syntax_tree.set_errors(self.line, self.column, error_description, environment.name, "semántico")

            return Symbol(self.line, self.column, None, Types.NULL)  # Se retorna el arreglo vacío.

        return Symbol(self.line, self.column, array_values, Types.ARRAY)  # Se retorna el arreglo con sus valores.
