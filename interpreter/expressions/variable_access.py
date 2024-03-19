from interpreter.interfaces.expression import Expression


class VariableAccess(Expression):
    def __init__(self, line, column, name):
        self.line = line
        self.column = column
        self.name = name

    def execute(self, syntax_tree, environment):
        symbol = environment.get_variable(self.line, self.column, syntax_tree, self.name)  # Se busca en el entorno.

        return symbol
