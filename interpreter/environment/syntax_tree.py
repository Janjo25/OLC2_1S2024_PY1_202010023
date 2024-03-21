class SyntaxTree:
    def __init__(self):
        self.console = ""
        self.errors = []
        self.instructions = []
        self.symbols = []

    def set_console(self, text):
        self.console += text + "\n"

    def get_console(self):
        return self.console

    def set_errors(self, line, column, description, scope, kind):
        error = {
            "line": line,
            "column": column,
            "description": description,
            "scope": scope,
            "kind": kind
        }

        self.errors.append(error)

    def get_errors(self):
        return self.errors

    def set_instructions(self, instruction):
        self.instructions += instruction

    def get_instructions(self):
        return self.instructions

    def set_symbols(self, name, symbol_kind, data_kind, scope, line, column):
        symbol = {
            "name": name,
            "symbol_kind": symbol_kind,
            "data_kind": data_kind,
            "scope": scope,
            "line": line,
            "column": column
        }

        self.symbols.append(symbol)

    def get_symbols(self):
        return self.symbols
