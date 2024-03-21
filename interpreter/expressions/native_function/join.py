from interpreter.environment.symbol import Symbol
from interpreter.environment.types import Types
from interpreter.interfaces.expression import Expression


class Join(Expression):
    def __init__(self, line, column, expression):
        self.line = line
        self.column = column
        self.expression = expression

    def execute(self, syntax_tree, environment):
        result = self.expression.execute(syntax_tree, environment)

        if result.kind == Types.ARRAY:
            string_elements = [str(element.value) for element in result.value]

            joined_value = ", ".join(string_elements)

            return Symbol(self.line, self.column, joined_value, Types.STRING)
        else:
            error_description = "la función 'join' solo puede ser aplicada a arreglos"

            syntax_tree.set_errors(self.line, self.column, error_description, environment.name, "semántico")

            return Symbol(self.line, self.column, None, Types.NULL)
