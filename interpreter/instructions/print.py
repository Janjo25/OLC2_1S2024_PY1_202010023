from interpreter.interfaces.instruction import Instruction


class Print(Instruction):
    def __init__(self, line, column, expressions):
        self.line = line
        self.column = column
        self.expressions = expressions

    def execute(self, syntax_tree, environment):
        output_text = ""

        for expression in self.expressions:  # Se recorren las expresiones.
            symbol = expression.execute(syntax_tree, environment)  # Se obtiene el símbolo que representa la expresión.

            output_text += " " + str(symbol.value)  # Se agrega un espacio en blanco para separar las expresiones.

        syntax_tree.set_console(output_text)  # Se agrega el texto al buffer de salida.
