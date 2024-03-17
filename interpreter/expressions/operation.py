from interpreter.environment.symbol import Symbol
from interpreter.environment.types import Types
from interpreter.interfaces.expression import Expression


class Operation(Expression):
    # noinspection DuplicatedCode
    arithmetic_matrix = [  # Tabla de tipos para saber el tipo que resulta de una operación aritmética.
        [Types.NUMBER, Types.FLOAT, Types.NULL, Types.NULL, Types.NULL],
        [Types.FLOAT, Types.FLOAT, Types.NULL, Types.NULL, Types.NULL],
        [Types.NULL, Types.NULL, Types.STRING, Types.NULL, Types.NULL],
        [Types.NULL, Types.NULL, Types.NULL, Types.NULL, Types.NULL],
        [Types.NULL, Types.NULL, Types.NULL, Types.NULL, Types.NULL]
    ]

    # noinspection DuplicatedCode
    relational_matrix = [  # Tabla de tipos para saber el tipo que resulta de una operación relacional.
        [Types.BOOLEAN, Types.NULL, Types.NULL, Types.NULL, Types.NULL],
        [Types.NULL, Types.BOOLEAN, Types.NULL, Types.NULL, Types.NULL],
        [Types.NULL, Types.NULL, Types.BOOLEAN, Types.NULL, Types.NULL],
        [Types.NULL, Types.NULL, Types.NULL, Types.BOOLEAN, Types.NULL],
        [Types.NULL, Types.NULL, Types.NULL, Types.NULL, Types.BOOLEAN]
    ]

    def __init__(self, line, column, operator, left_operand, right_operand):
        self.line = line
        self.column = column
        self.operator = operator
        self.left_operand = left_operand
        self.right_operand = right_operand

    def execute(self, syntax_tree, environment):
        left_operand = self.left_operand.execute(syntax_tree, environment)
        right_operand = self.right_operand.execute(syntax_tree, environment)

        left_type = left_operand.kind.name
        right_type = right_operand.kind.name

        dominant_type = Types.NULL

        if self.operator in {'+', '-', '*', '/', '%'}:
            dominant_type = Operation.arithmetic_matrix[left_operand.kind.value][right_operand.kind.value]
        elif self.operator in {'==', '!=', '>', '>=', '<', '<='}:
            dominant_type = Operation.relational_matrix[left_operand.kind.value][right_operand.kind.value]

        if self.operator in {'+', '-', '*', '/', '%'}:
            if dominant_type == Types.NULL:
                error_description = "los tipos " + left_type + " y " + right_type + " no son compatibles"
                syntax_tree.set_errors(self.line, self.column, error_description, environment.name, "semántico")

                return Symbol(self.line, self.column, None, Types.NULL)

            return self.arithmetic_operation(syntax_tree, environment, left_operand, right_operand, dominant_type)
        elif self.operator in {'==', '!=', '>', '>=', '<', '<='}:
            if left_operand.kind != right_operand.kind:
                error_description = "los tipos " + left_type + " y " + right_type + " no son compatibles"
                syntax_tree.set_errors(self.line, self.column, error_description, environment.name, "semántico")

                return Symbol(self.line, self.column, None, Types.NULL)

            return self.relational_operation(left_operand, right_operand)

    def arithmetic_operation(self, syntax_tree, environment, left_operand, right_operand, dominant_type):
        if dominant_type == Types.NUMBER or dominant_type == Types.FLOAT or dominant_type == Types.STRING:
            if self.operator == '+':
                return Symbol(self.line, self.column, left_operand.value + right_operand.value, dominant_type)

        if dominant_type == Types.NUMBER or dominant_type == Types.FLOAT:
            if self.operator == '-':
                return Symbol(self.line, self.column, left_operand.value - right_operand.value, dominant_type)
            elif self.operator == '*':
                return Symbol(self.line, self.column, left_operand.value * right_operand.value, dominant_type)
            elif self.operator in {'/', '%'}:
                if right_operand.value == 0:
                    error_description = "no se puede dividir entre cero"
                    syntax_tree.set_errors(self.line, self.column, error_description, environment.name, "semántico")

                    return Symbol(self.line, self.column, None, Types.NULL)

                if self.operator == '/':
                    return Symbol(self.line, self.column, left_operand.value / right_operand.value, dominant_type)
                elif self.operator == '%':
                    return Symbol(self.line, self.column, left_operand.value % right_operand.value, dominant_type)

        left_type = left_operand.kind.name
        right_type = right_operand.kind.name
        error_description = "los tipos '" + left_type + "' y '" + right_type + "' no son compatibles"

        syntax_tree.set_errors(self.line, self.column, error_description, environment.name, "semántico")

        return Symbol(self.line, self.column, None, Types.NULL)

    def relational_operation(self, left_operand, right_operand):
        if self.operator == '==':
            return Symbol(self.line, self.column, left_operand.value == right_operand.value, Types.BOOLEAN)
        elif self.operator == '!=':
            return Symbol(self.line, self.column, left_operand.value != right_operand.value, Types.BOOLEAN)
        elif self.operator == '>':
            return Symbol(self.line, self.column, left_operand.value > right_operand.value, Types.BOOLEAN)
        elif self.operator == '<':
            return Symbol(self.line, self.column, left_operand.value < right_operand.value, Types.BOOLEAN)
        elif self.operator == '>=':
            return Symbol(self.line, self.column, left_operand.value >= right_operand.value, Types.BOOLEAN)
        elif self.operator == '<=':
            return Symbol(self.line, self.column, left_operand.value <= right_operand.value, Types.BOOLEAN)
