from interpreter.environment.symbol import Symbol
from interpreter.environment.types import Types
from interpreter.interfaces.expression import Expression


class Keys(Expression):
    def __init__(self, line, column, expression):
        self.line = line
        self.column = column
        self.expression = expression

    def execute(self, syntax_tree, environment):
        result = self.expression.execute(syntax_tree, environment)

        if result.kind == Types.INTERFACE:
            keys = list(result.value.keys())

            for key in range(len(keys)):  # Las llaves se convierten en su símbolo correspondiente.
                keys[key] = Symbol(self.line, self.column, keys[key], Types.STRING)

            return Symbol(self.line, self.column, keys, Types.ARRAY)
        else:
            raise Exception(f"tipo inválido '{result.kind}' para función 'keys'.")
