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

        constant_name = f"{name}-constant"  # Con este nombre se intentará buscar la constante en la tabla de símbolos.

        while True:
            if name in current_environment.table or constant_name in current_environment.table:
                """Se debe de obtener el verdadero nombre, con o sin el sufijo '-constant'."""

                actual_name = name if name in current_environment.table else constant_name

                if actual_name == constant_name:  # Si el verdadero nombre es el de la constante, no se puede modificar.
                    error_description = f"no es posible modificar el valor de la constante '{name}'"

                    syntax_tree.set_errors(line, column, error_description, current_environment.name, "semántico")

                    return

                stored_symbol = current_environment.table[actual_name]  # Se obtiene el símbolo almacenado.

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

        constant_name = f"{name}-constant"  # Con este nombre se intentará buscar la constante en la tabla de símbolos.

        while True:
            if name in current_environment.table or constant_name in current_environment.table:
                actual_name = name if name in current_environment.table else constant_name

                return current_environment.table[actual_name]

            if current_environment.previous is None:  # Si no existe un entorno anterior, se rompe el ciclo.
                break
            else:  # Si existe un entorno anterior, se convierte en el entorno actual.
                current_environment = current_environment.previous

        syntax_tree.set_errors(line, column, f"la variable '{name}' no existe", current_environment.name, "semántico")

        return Symbol('-', '-', None, Types.NULL)

    def check_variable(self, syntax_tree, name, symbol):
        if name in self.table:  # Se revisa en la tabla de símbolos si ya existe la variable.
            line = symbol.line
            column = symbol.column

            syntax_tree.set_errors(line, column, f"la variable '{name}' ya existe", self.name, "sintáctico")

            return

        self.table[name] = symbol  # Si no existe, se agrega a la tabla de símbolos.

        syntax_tree.set_symbols(name, "variable", symbol.kind, self.name, symbol.line, symbol.column)

    def set_interface(self, syntax_tree, interface_path, symbol):
        path_fields = interface_path.split('.')  # Se separa la ruta en partes.
        base_symbol = self.get_variable('-', '-', syntax_tree, path_fields[0])  # Se obtiene el símbolo base.

        if base_symbol.kind != Types.INTERFACE:
            error_description = f"'la variable '{path_fields[0]}' no es una interfaz"

            syntax_tree.set_errors('-', '-', error_description, self.name, "semántico")

            return

        """Se procede a 'navegar' por los campos de la interfaz para llegar al campo final."""

        current_symbol = base_symbol

        for field in path_fields[1:-1]:  # Se recorren todos los campos menos el último, porque es el que se modificará.
            if field not in current_symbol.value:
                error_description = f"el campo '{field}' no existe en '{current_symbol.name}'"

                syntax_tree.set_errors('-', '-', error_description, self.name, "semántico")

                return

            current_symbol = current_symbol.value[field]  # Se obtiene el símbolo del campo actual.

        final_field = path_fields[-1]

        if final_field not in current_symbol.value:  # Se revisa si el campo final existe en la interfaz.
            error_description = f"el campo '{final_field}' no existe en '{current_symbol.name}'"

            syntax_tree.set_errors('-', '-', error_description, self.name, "semántico")

            return

        current_symbol.value[final_field] = symbol  # Se actualiza el campo final con el nuevo valor.

    def get_interface(self, syntax_tree, name):
        current_environment = self

        while True:
            if name in current_environment.interfaces:
                return current_environment.interfaces[name]

            if current_environment.previous is None:  # struct_instantiation
                break
            else:
                current_environment = current_environment.previous

        syntax_tree.set_errors('-', '-', f"la interfaz '{name}' no existe", current_environment.name, "semántico")

        return None

    def check_interface(self, line, column, syntax_tree, name, interface):
        if name in self.interfaces:
            error_description = f"la interfaz '{name}' ya existe"

            syntax_tree.set_errors(interface.line, interface.column, error_description, self.name, "sintáctico")

            return

        self.interfaces[name] = interface

        syntax_tree.set_symbols(name, "interfaz", '-', self.name, line, column)

    def get_function(self, syntax_tree, name):
        current_environment = self

        function_name = f"{name}-function"  # Con este nombre se intentará buscar la función en la tabla de funciones.

        while True:
            if function_name in current_environment.functions:
                return current_environment.functions[function_name]

            if current_environment.previous is None:
                break
            else:
                current_environment = current_environment.previous

        syntax_tree.set_errors('-', '-', f"la función '{name}' no existe", current_environment.name, "semántico")

        return None

    def check_function(self, line, column, syntax_tree, name, function):
        if name in self.functions:
            error_description = f"la función '{name}' ya existe"

            syntax_tree.set_errors(function.line, function.column, error_description, self.name, "sintáctico")

            return

        self.functions[name] = function

        syntax_tree.set_symbols(name, "función", function["kind"], self.name, line, column)

    def is_within_control_flow(self):
        control_flow_environments = ["case", "for", "switch", "while"]

        current_environment = self

        while True:
            if current_environment.name in control_flow_environments:  # Se revisa si el entorno es un flujo de control.
                return True

            if current_environment.previous is None:  # Si no existe un entorno anterior, se rompe el ciclo.
                break
            else:  # Si existe un entorno anterior, se convierte en el entorno actual.
                current_environment = current_environment.previous

        return False

    def is_within_function(self):
        current_environment = self

        while True:
            if current_environment.name.endswith("-function"):  # Se revisa si el entorno es una función.
                return True

            if current_environment.previous is None:  # Si no existe un entorno anterior, se rompe el ciclo.
                break
            else:  # Si existe un entorno anterior, se convierte en el entorno actual.
                current_environment = current_environment.previous

        return False
