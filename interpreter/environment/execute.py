from interpreter.environment.types import Types

"""Esta función ejecuta las instrucciones de un bloque de código."""


def instructions_executor(instructions, syntax_tree, environment):
    for instruction in instructions:
        symbol = instruction.execute(syntax_tree, environment)

        if symbol is not None:
            if symbol.kind == Types.RETURN:
                return symbol.value

            return symbol

    return None
