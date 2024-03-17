from interpreter.interfaces.instruction import Instruction


class TernaryOperator(Instruction):
    def __init__(self, line, column, condition_expression, true_expression, false_expression):
        self.line = line
        self.column = column
        self.condition_expression = condition_expression  # Expresión que se evalúa para saber cuál se ejecuta.
        self.true_expression = true_expression  # Expresión que se ejecuta si la condición es verdadera.
        self.false_expression = false_expression  # Expresión que se ejecuta si la condición es falsa.

    def execute(self, syntax_tree, environment):
        condition = self.condition_expression.execute(syntax_tree, environment)

        if condition.value is True:
            return self.true_expression.execute(syntax_tree, environment)
        else:
            return self.false_expression.execute(syntax_tree, environment)
