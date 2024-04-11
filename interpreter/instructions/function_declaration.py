from interpreter.interfaces.instruction import Instruction


class FunctionDeclaration(Instruction):
    def __init__(self, line, column, name, instructions, kind=None, parameters=None):
        self.line = line
        self.column = column
        self.name = name
        self.instructions = instructions
        self.kind = kind

        if parameters is None:  # Si no se especifican parámetros, se inicializa como una lista vacía.
            parameters = []

        self.parameters = parameters

    def execute(self, syntax_tree, environment):
        """Se crea un diccionario con la información de la función que luego se usará para ejecutarla."""

        function_data = {"instructions": self.instructions, "kind": self.kind, "parameters": self.parameters}

        environment.check_function(self.line, self.column, syntax_tree, self.name, function_data)

        return None
