"""Para facilitar el manejo de expresiones, todas se convertirán a objetos de tipo 'Symbol'."""


class Symbol:
    def __init__(self, line, column, value, kind):  # Se usa 'kind' porque 'type' es una palabra reservada.
        self.line = line
        self.column = column
        self.value = value
        self.kind = kind
