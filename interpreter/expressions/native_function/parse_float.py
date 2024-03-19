from interpreter.environment.symbol import Symbol
from interpreter.environment.types import Types
from interpreter.interfaces.expression import Expression


class ParseFloat(Expression):
    def __init__(self, line, column, expression):
        self.line = line
        self.column = column
        self.expression = expression

        """Los datos en los entornos deben de manipularse con mucho cuidado, ya que una modificación puede ser general.
           Por ejemplo, si a la variable 'result' se le modifica su valor, este cambio se verá reflejado en la tabla.
           Esto ocurre porque al encontrar la variable en la tabla, se retorna la referencia a la misma, no una copia.
           Por lo que si se modifica el valor de la variable, se modificará en la tabla de símbolos.
           Para evitar este comportamiento, se debe de crear un nuevo símbolo con el valor modificado y retornarlo."""

    def execute(self, syntax_tree, environment):
        result = self.expression.execute(syntax_tree, environment)

        try:
            parsed_value = float(result.value)  # Se intenta convertir el valor a flotante.

            return Symbol(self.line, self.column, parsed_value, Types.FLOAT)
        except ValueError:  # Si no se puede convertir el valor a flotante, se retorna un valor nulo.
            error_description = 'no fue posible convertir el valor a float'

            syntax_tree.set_errors(self.line, self.column, error_description, environment.name, "semántico")

            return Symbol(self.line, self.column, None, Types.NULL)
