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

        dominant_type = dominant_matrix[left_operand.kind.value][right_operand.kind.value]

        if self.operator == '+':
            if dominant_type == Types.NUMBER or dominant_type == Types.FLOAT or dominant_type == Types.STRING:
                symbol = Symbol(self.line, self.column, left_operand.value + right_operand.value, dominant_type)

                return symbol

            syntax_tree.set_errors("para sumar, los operandos deben ser de tipo number, float o string")

        if self.operator == "-":
            if dominant_type == Types.NUMBER or dominant_type == Types.FLOAT:
                return Symbol(self.line, self.column, left_operand.value - right_operand.value, dominant_type)

            syntax_tree.set_errors("para restar, los operandos deben ser de tipo number o float")

        if self.operator == "*":
            if dominant_type == Types.NUMBER or dominant_type == Types.FLOAT:
                return Symbol(self.line, self.column, left_operand.value * right_operand.value, dominant_type)

            syntax_tree.set_errors("para multiplicar, los operandos deben ser de tipo number o float")

        if self.operator == "/":
            if right_operand.value == 0:
                syntax_tree.set_errors("no se puede dividir entre 0")

                return

            if dominant_type == Types.NUMBER or dominant_type == Types.FLOAT:
                return Symbol(self.line, self.column, left_operand.value / right_operand.value, dominant_type)

            syntax_tree.set_errors("para dividir, los operandos deben ser de tipo number o float")

        if self.operator == "%":
            if dominant_type == Types.NUMBER or dominant_type == Types.FLOAT:
                return Symbol(self.line, self.column, left_operand.value % right_operand.value, dominant_type)

            syntax_tree.set_errors("para dividir, los operandos deben ser de tipo number o float")

        return Symbol(self.line, self.column, None, Types.NULL)
