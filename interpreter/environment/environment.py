from interpreter.environment.symbol import Symbol
from interpreter.environment.types import Types


class Environment:
    def __init__(self, previous, name):
        self.previous = previous
        self.name = name

        self.functions = {}
        self.interfaces = {}
        self.table = {}

    def set_variable(self, syntax_tree, name, symbol):
        current_environment = self

        line = symbol.line
        column = symbol.column

        while True:
            if name in current_environment.table:
                stored_symbol = current_environment.table[name]  # Se obtiene el símbolo almacenado.

                if stored_symbol.kind != symbol.kind:  # Se revisa si la variable ya existe con un tipo diferente.
                    if stored_symbol.kind == Types.FLOAT and symbol.kind == Types.NUMBER:
                        symbol.value = float(symbol.value)  # Se realiza una conversión implícita de número a flotante.
                        symbol.kind = Types.FLOAT

                        current_environment.table[name] = symbol

                        return symbol

                    symbol.value = None  # Si el tipo es diferente, se le asigna un valor nulo al símbolo existente.
                    symbol.kind = Types.NULL

                    current_environment.table[name] = symbol

                    error_description = f"la variable '{name}' ya existe con un tipo diferente"

                    syntax_tree.set_errors(line, column, error_description, current_environment.name, "semántico")

                    return symbol

                current_environment.table[name] = symbol  # Se revisa en la tabla de símbolos si ya existe la variable.

                return symbol  # Si ya existe, se edita el símbolo en la tabla de símbolos.

            if current_environment.previous is None:  # Si no existe un entorno anterior, se rompe el ciclo.
                break
            else:  # Si existe un entorno anterior, se convierte en el entorno actual.
                current_environment = current_environment.previous

        syntax_tree.set_errors(line, column, f"la variable '{name}' no existe", current_environment.name, "semántico")

        return Symbol(symbol.line, symbol.column, None, Types.NULL)

    def get_variable(self, line, column, syntax_tree, name):
        current_environment = self

        while True:
            if name in current_environment.table:  # Se revisa en la tabla de símbolos si ya existe la variable.
                return current_environment.table[name]

            if current_environment.previous is None:  # Si no existe un entorno anterior, se rompe el ciclo.
                break
            else:  # Si existe un entorno anterior, se convierte en el entorno actual.
                current_environment = current_environment.previous

        syntax_tree.set_errors(line, column, f"la variable '{name}' no existe", current_environment.name, "semántico")

        return Symbol("-", "-", None, Types.NULL)

    def check_variable(self, syntax_tree, name, symbol):
        if name in self.table:  # Se revisa en la tabla de símbolos si ya existe la variable.
            syntax_tree.set_errors(symbol.line, symbol.column, f"la variable '{name}' ya existe", "semántico")

            return

        self.table[name] = symbol  # Si no existe, se agrega a la tabla de símbolos.
