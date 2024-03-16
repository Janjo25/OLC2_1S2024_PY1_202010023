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
            line = symbol.line
            column = symbol.column
            error_description = f"el tipo de dato de la variable '{self.name}' no coincide con el tipo de dato"

            syntax_tree.set_errors(line, column, error_description, environment.name, "semántico")

            symbol.value = None  # Ya que el tipo de dato no coincide, se le asigna un valor nulo.

            environment.check_variable(syntax_tree, self.name, symbol)  # Se revisa si existe en la tabla de símbolos.

            return

        environment.check_variable(syntax_tree, self.name, symbol)  # Se revisa si existe en la tabla de símbolos.
