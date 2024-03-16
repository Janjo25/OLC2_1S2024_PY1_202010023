from interpreter.environment.symbol import Symbol
from interpreter.environment.types import Types
from interpreter.interfaces.expression import Expression

dominant_matrix = [  # Esto es una tabla de tipos, se usa para saber el tipo resultante de una operación.
    [Types.NUMBER, Types.FLOAT, Types.NULL, Types.NULL, Types.NULL],
    [Types.FLOAT, Types.FLOAT, Types.NULL, Types.NULL, Types.NULL],
    [Types.NULL, Types.NULL, Types.STRING, Types.NULL, Types.NULL],
    [Types.NULL, Types.NULL, Types.NULL, Types.NULL, Types.NULL],
    [Types.NULL, Types.NULL, Types.NULL, Types.NULL, Types.NULL]
]


class Operation(Expression):
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

        dominant_type = dominant_matrix[left_operand.kind.value][right_operand.kind.value]

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
        if self.operator == '+':
            return Symbol(self.line, self.column, left_operand.value + right_operand.value, dominant_type)
        elif self.operator == '-':
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
