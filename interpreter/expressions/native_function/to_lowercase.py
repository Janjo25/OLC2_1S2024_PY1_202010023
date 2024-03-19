from interpreter.environment.symbol import Symbol
from interpreter.environment.types import Types
from interpreter.interfaces.expression import Expression


class ToLowerCase(Expression):
    def __init__(self, line, column, expression):
        self.line = line
        self.column = column
        self.expression = expression

    def execute(self, syntax_tree, environment):
        result = self.expression.execute(syntax_tree, environment)

        if result.kind == Types.STRING:
            lowercase_value = result.value.lower()

            return Symbol(self.line, self.column, lowercase_value, Types.STRING)
        else:
            error_description = "el tipo de dato no es compatible con la función 'toLowerCase'"

            syntax_tree.set_errors(self.line, self.column, error_description, environment.name, "semántico")

            return Symbol(self.line, self.column, None, Types.NULL)
