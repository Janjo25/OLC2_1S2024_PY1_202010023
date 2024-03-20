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

            if isinstance(symbol.value, list):  # Si el valor del símbolo es una lista, se recorre cada elemento.
                output_text += '['

                for i in range(len(symbol.value)):
                    if i != 0:  # Si no es el primer elemento, se agrega una coma.
                        output_text += ", "

                    output_text += str(symbol.value[i].value)

                output_text += ']'

                continue

            output_text += " " + str(symbol.value)  # Se agrega un espacio en blanco para separar las expresiones.

        syntax_tree.set_console(output_text.strip())  # Se agrega el texto al buffer de salida.
