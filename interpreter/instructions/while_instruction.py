from interpreter.environment.environment import Environment
from interpreter.environment.execute import instructions_executor
from interpreter.environment.symbol import Symbol
from interpreter.environment.types import Types
from interpreter.interfaces.instruction import Instruction


class WhileInstruction(Instruction):
    def __init__(self, line, column, condition, instructions):
        self.line = line
        self.column = column
        self.condition = condition
        self.instructions = instructions

    def execute(self, syntax_tree, environment):
        while self.condition.execute(syntax_tree, environment).value:
            while_environment = Environment(environment, "while")

            result = instructions_executor(self.instructions, syntax_tree, while_environment)

            if isinstance(result, Symbol):
                if result.kind == Types.BREAK:
                    break
                if result.kind == Types.CONTINUE:
                    continue
                if result.kind == Types.RETURN:
                    return result
