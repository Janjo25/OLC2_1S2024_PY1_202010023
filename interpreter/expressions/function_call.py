from interpreter.environment.environment import Environment
from interpreter.environment.execute import instructions_executor
from interpreter.environment.symbol import Symbol
from interpreter.environment.types import Types
from interpreter.interfaces.expression import Expression


class FunctionCall(Expression):
    def __init__(self, line, column, name, parameters=None):
        self.line = line
        self.column = column
        self.name = name

        if parameters is None:  # Si no se especifican parámetros, se inicializa la lista de parámetros como vacía.
            parameters = []

        self.parameters = parameters

    def execute(self, syntax_tree, environment):
        function_data = environment.get_function(syntax_tree, self.name)

        if function_data is None:  # Se verifica si la función existe en la tabla de funciones.
            error_description = f"la función '{self.name}' no existe"

            syntax_tree.set_errors(self.line, self.column, error_description, environment.name, "semántico")

            return Symbol("-", "-", None, Types.NULL)

        """Se procede a evaluar los parámetros de la función."""

        evaluated_parameters = [parameter.execute(syntax_tree, environment) for parameter in self.parameters]

        function_environment = Environment(environment, f"{self.name}-function")

        for parameter_dictionary, evaluated_parameter in zip(function_data["parameters"], evaluated_parameters):
            parameter_name = next(iter(parameter_dictionary))  # Se obtiene el nombre del parámetro.

            function_environment.check_variable(syntax_tree, parameter_name, evaluated_parameter)

        result = instructions_executor(function_data["instructions"], syntax_tree, function_environment)

        if result is not None:
            return result
