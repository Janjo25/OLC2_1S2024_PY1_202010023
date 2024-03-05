from interpreter.interfaces.instruction import Instruction


class Declaration(Instruction):
    def __init__(self, line, column, name, kind, expressions):
        self.line = line
        self.column = column
        self.name = name
        self.kind = kind
        self.expressions = expressions

    def execute(self, syntax_tree, environment):
        symbol = self.expressions.execute(syntax_tree, environment)

        if symbol.kind != self.kind:
            syntax_tree.set_errors("el tipo de la variable no coincide con el tipo de la expresión")

            return

        environment.check_variable(syntax_tree, self.name, symbol)  # Se revisa si existe en la tabla de símbolos.
