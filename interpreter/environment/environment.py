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

        while True:
            if name in current_environment.table:
                current_environment.table[name] = symbol  # Se revisa en la tabla de símbolos si ya existe la variable.

                return symbol  # Si ya existe, se edita el símbolo en la tabla de símbolos.

            if current_environment.previous is None:  # Si no existe un entorno anterior, se rompe el ciclo.
                break
            else:  # Si existe un entorno anterior, se convierte en el entorno actual.
                current_environment = current_environment.previous

        syntax_tree.set_errors(f"la variable '{name}' no existe")  # Se retorna 'null' si no existe la variable.

        return Symbol(0, 0, None, Types.NULL)

    def get_variable(self, syntax_tree, name):
        current_environment = self

        while True:
            if name in current_environment.table:  # Se revisa en la tabla de símbolos si ya existe la variable.
                return current_environment.table[name]

            if current_environment.previous is None:  # Si no existe un entorno anterior, se rompe el ciclo.
                break
            else:  # Si existe un entorno anterior, se convierte en el entorno actual.
                current_environment = current_environment.previous

        syntax_tree.set_errors(f"la variable '{name}' no existe")  # Se retorna 'null' si no existe la variable.

        return Symbol(0, 0, None, Types.NULL)

    def check_variable(self, syntax_tree, name, symbol):
        if name in self.table:  # Se revisa en la tabla de símbolos si ya existe la variable.
            syntax_tree.set_errors(f"la variable '{name}' ya existe")

            return

        self.table[name] = symbol  # Si no existe, se agrega a la tabla de símbolos.
