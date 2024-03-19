import ply.lex as lex
import ply.yacc as yacc

from interpreter.environment.types import Types
from interpreter.expressions.access import VariableAccess
from interpreter.expressions.break_statement import BreakStatement
from interpreter.expressions.continue_statement import ContinueStatement
from interpreter.expressions.operation import Operation
from interpreter.expressions.primitive import Primitive
from interpreter.expressions.return_statement import ReturnStatement
from interpreter.expressions.ternary_operator import TernaryOperator
from interpreter.instructions.assignment import Assignment
from interpreter.instructions.declaration import Declaration
from interpreter.instructions.for_instruction import ForInstruction
from interpreter.instructions.if_instruction import IfInstruction
from interpreter.instructions.print import Print
from interpreter.instructions.switch_instruction import SwitchInstruction
from interpreter.instructions.while_instruction import WhileInstruction


class Interpreter:
    def __init__(self):
        self.lexer = lex.lex()
        self.parser = yacc.yacc()

    def interpret(self, input_text):
        return self.parser.parse(input_text)


default_values = {
    Types.NUMBER: 0,
    Types.FLOAT: 0.0,
    Types.STRING: "",
    Types.BOOLEAN: True,
    Types.CHAR: ''
}

# noinspection SpellCheckingInspection
reserved = {
    "Keys": "KEYS", "Object": "OBJECT", "Values": "VALUES", "array": "ARRAY", "boolean": "BOOLEAN",
    "break": "BREAK", "case": "CASE", "char": "CHAR", "console": "CONSOLE", "const": "CONST",
    "continue": "CONTINUE", "default": "DEFAULT", "else": "ELSE", "false": "FALSE", "float": "FLOAT",
    "for": "FOR", "function": "FUNCTION", "if": "IF", "indexOf": "INDEXOF", "interface": "INTERFACE",
    "join": "JOIN", "length": "LENGTH", "log": "LOG", "null": "NULL", "number": "NUMBER", "of": "OF",
    "parseFloat": "PARSEFLOAT", "parseInt": "PARSEINT", "pop": "POP", "push": "PUSH", "return": "RETURN",
    "string": "STRING", "switch": "SWITCH", "toLowerCase": "TOLOWERCASE", "toString": "TOSTRING",
    "toUpperCase": "TOUPPERCASE", "true": "TRUE", "typeof": "TYPEOF", "var": "VAR", "while": "WHILE"
}

# noinspection SpellCheckingInspection
tokens = [
    "AND", "ASSIGN", "COLON", "COMMA", "COMMENT_MULTI", "COMMENT_SINGLE", "DECREMENT", "DIVIDE", "DOT", "EQ",
    "GE", "GT", "IDENTIFIER", "INCREMENT", "LBRACE", "LBRACKET", "LE", "LPAREN", "LT", "MINUS", "MINUSEQUAL",
    "MOD", "NEQ", "NOT", "OR", "PLUS", "PLUSEQUAL", "QUESTION", "RBRACE", "RBRACKET", "RPAREN", "SEMICOLON",
    "TIMES"
]

tokens += list(reserved.values())

"""Agrupación y Puntuación"""

t_COLON = r":"
t_COMMA = r","
t_DOT = r"\."
t_LBRACE = r"\{"
t_LBRACKET = r"\["
t_LPAREN = r"\("
t_RBRACE = r"\}"
t_RBRACKET = r"\]"
t_RPAREN = r"\)"
t_SEMICOLON = r";"

"""Operadores Aritméticos"""

t_DIVIDE = r"/"
t_MINUS = r"-"
t_MOD = r"%"
t_PLUS = r"\+"
t_TIMES = r"\*"

"""Operadores Comparativos"""

t_EQ = r"=="
t_GE = r">="
t_GT = r">"
t_LE = r"<="
t_LT = r"<"
t_NEQ = r"!="

"""Operadores Condicionales"""

t_QUESTION = r"\?"

"""Operadores Lógicos"""

t_AND = r"&&"
t_NOT = r"!"
t_OR = r"\|\|"

"""Operadores de Asignación"""

t_ASSIGN = r"="
t_DECREMENT = r"--"
t_INCREMENT = r"\+\+"
t_MINUSEQUAL = r"-="
t_PLUSEQUAL = r"\+="


def find_column(input_text, token):  # Función para encontrar la columna de un token.
    line_start = input_text.rfind("\n", 0, token.lexpos) + 1

    return (token.lexpos - line_start) + 1


# noinspection PyPep8Naming
def t_BOOLEAN(t):  # Función para reconocer booleanos.
    r"""true|false"""
    try:
        t.value = True if t.value == "true" else False

        line = t.lineno
        column = find_column(t.lexer.lexdata, t)

        t.value = Primitive(line, column, t.value, Types.BOOLEAN)
    except ValueError:
        t.value = Primitive(0, 0, None, Types.NULL)

        print(f"booleano no válido en la línea {t.lineno}, columna {find_column(t.lexer.lexdata, t)}.")

    return t


# noinspection DuplicatedCode,PyPep8Naming
def t_CHAR(t):  # Función para reconocer caracteres.
    r"""'(?:\\['\\]|[^\n'\\])'"""
    try:
        t.value = bytes(t.value[1:-1], "utf-8").decode("unicode_escape")  # Se decodifican las secuencias de escape.

        line = t.lineno
        column = find_column(t.lexer.lexdata, t)

        t.value = Primitive(line, column, t.value, Types.CHAR)
    except ValueError:
        t.value = Primitive(0, 0, None, Types.NULL)

        print(f"carácter no válido en la línea {t.lineno}, columna {find_column(t.lexer.lexdata, t)}.")

    return t


# noinspection PyPep8Naming
def t_COMMENT_MULTI(t):  # Función para reconocer comentarios de múltiples líneas.
    r"""/\*(.|\n)*?\*/"""
    t.lexer.lineno += t.value.count("\n")  # Se aumenta el número de línea por cada salto de línea en el comentario.


# noinspection PyPep8Naming,PyUnusedLocal
def t_COMMENT_SINGLE(t):  # Función para reconocer comentarios de una línea.
    r"""//.*"""
    pass


# noinspection PyPep8Naming
def t_FLOAT(t):  # Función para reconocer flotantes.
    r"""\d+\.\d+"""
    try:
        t.value = float(t.value)

        line = t.lineno
        column = find_column(t.lexer.lexdata, t)

        t.value = Primitive(line, column, t.value, Types.FLOAT)
    except ValueError:
        t.value = Primitive(0, 0, None, Types.NULL)

        print(f"número decimal no válido en la línea {t.lineno}, columna {find_column(t.lexer.lexdata, t)}.")

    return t


# noinspection PyPep8Naming
def t_IDENTIFIER(t):  # Función para reconocer identificadores.
    r"""[a-zA-Z_][a-zA-Z_0-9]*"""
    t.type = reserved.get(t.value, "IDENTIFIER")  # Se verifica si el identificador es una palabra reservada.

    return t


# noinspection PyPep8Naming
def t_NULL(t):  # Función para reconocer nulos.
    r"""null"""
    t.value = None  # No es necesario un try-except, ya que no hay posibilidad de error.

    line = t.lineno
    column = find_column(t.lexer.lexdata, t)

    t.value = Primitive(line, column, None, Types.NULL)

    return t


# noinspection PyPep8Naming
def t_NUMBER(t):  # Función para reconocer números.
    r"""\d+"""
    try:
        t.value = int(t.value)

        line = t.lineno
        column = find_column(t.lexer.lexdata, t)

        t.value = Primitive(line, column, t.value, Types.NUMBER)
    except ValueError:
        t.value = Primitive(0, 0, None, Types.NULL)

        print(f"número no válido en la línea {t.lineno}, columna {find_column(t.lexer.lexdata, t)}.")

    return t


# noinspection DuplicatedCode,PyPep8Naming
def t_STRING(t):  # Función para reconocer cadenas.
    r""""(?:\\.|[^"\\])*\""""
    try:
        t.value = bytes(t.value[1:-1], "utf-8").decode("unicode_escape")  # Se decodifican las secuencias de escape.

        line = t.lineno
        column = find_column(t.lexer.lexdata, t)

        t.value = Primitive(line, column, t.value, Types.STRING)
    except ValueError:
        t.value = Primitive(0, 0, None, Types.NULL)

        print(f"cadena no válida en la línea {t.lineno}, columna {find_column(t.lexer.lexdata, t)}.")

    return t


t_ignore = " \t"


def t_newline(t):  # Función para reconocer saltos de línea.
    r"""\n+"""
    t.lexer.lineno += len(t.value)


def t_error(t):  # Función para manejar errores léxicos.
    print(f"carácter no válido '{t.value[0]}' en la línea {t.lineno}, columna {find_column(t.lexer.lexdata, t)}.")

    t.lexer.skip(1)  # Se salta el carácter no válido.


precedence = (
    ("left", "LPAREN", "RPAREN", "LBRACKET", "RBRACKET"),  # () []
    ("right", "NOT", "MINUS"),  # ! -
    ("left", "DIVIDE", "MOD", "TIMES"),  # / % *
    ("left", "PLUS", "MINUS"),  # + -
    ("left", "LT", "LE", "GT", "GE"),  # < <= > >=
    ("left", "EQ", "NEQ"),  # == !=
    ("left", "AND"),  # &&
    ("left", "OR"),  # ||
)

"""Cuando se usa 'p[0] = p[x] + [p[y]]', se está concatenando listas."""


def p_program(p):
    """program : statements"""
    p[0] = p[1]


def p_statements(p):
    """statements : statement
                  | statements statement"""
    if len(p) == 2:  # Si solo hay 2 elementos, entonces solo hay una instrucción.
        p[0] = [p[1]]
    else:  # Si hay más de 2 elementos, entonces hay más de una instrucción.
        p[0] = p[1] + [p[2]]


def p_statement(p):
    """statement : constant_declaration
                 | expression_statement
                 | flow_statements
                 | function_declaration
                 | transfer_statement
                 | variable_assignment
                 | variable_declaration"""
    p[0] = p[1]


# noinspection DuplicatedCode
def p_constant_declaration(p):
    """constant_declaration : CONST IDENTIFIER ASSIGN expression SEMICOLON
                            | CONST IDENTIFIER COLON type ASSIGN expression SEMICOLON"""
    line = p.lexer.lineno
    column = find_column(p.lexer.lexdata, p.lexer)

    constant_name = f"{p[2]}-constant"  # Se le agrega un sufijo para diferenciarla de las variables.

    if len(p) == 6:  # Si hay 6 elementos, entonces no hay un tipo o un valor.
        p[0] = Declaration(line, column, constant_name, p[4].kind, p[4])
    else:  # Si hay más de 6 elementos, entonces hay un tipo y un valor.
        if p[4] == Types.FLOAT and p[6].kind == Types.NUMBER:  # Se hace una conversión implícita de número a flotante.
            p[6].value = float(p[6].value)
            p[6].kind = Types.FLOAT

        p[0] = Declaration(line, column, constant_name, p[4], p[6])


def p_expression_statement(p):
    """expression_statement : expression SEMICOLON"""
    p[0] = p[1]


def p_expression(p):
    """expression : IDENTIFIER
                  | IDENTIFIER LPAREN arguments RPAREN
                  | LPAREN expression RPAREN
                  | binary_operation
                  | native_function
                  | primitive
                  | ternary_operator
                  | unary_operation"""
    if len(p) == 2:  # Si solo hay 2 elementos, entonces es un ID o un no-terminal.
        if p.slice[1].type == "IDENTIFIER":
            line = p.lexer.lineno
            column = find_column(p.lexer.lexdata, p.lexer)

            p[0] = VariableAccess(line, column, p[1])
        else:
            p[0] = p[1]
    elif len(p) == 3:  # Si hay 3 elementos, entonces es una negación.
        p[0] = ("not_expression", p[2])
    elif len(p) == 4:  # Si hay 4 elementos, entonces es una expresión entre paréntesis.
        p[0] = p[2]
    else:  # Si hay 5 elementos, entonces es una llamada a función.
        p[0] = ("function_call", p[1], p[3])


def p_arguments(p):
    """arguments : argument
                 | arguments COMMA argument"""
    if len(p) == 2:  # Si solo hay 2 elementos, entonces solo hay un argumento.
        p[0] = [p[1]]  # Se debe de retornar una lista para que sea iterable y no cause problemas más adelante.
    else:  # Si hay más de 2 elementos, entonces hay más de un argumento.
        p[0] = p[1] + [p[3]]


def p_argument(p):
    """argument : expression"""
    p[0] = p[1]


def p_binary_operation(p):
    """binary_operation : expression arithmetic_operator expression
                        | expression comparison_operator expression
                        | expression logical_operator expression"""
    line = p.lexer.lineno
    column = find_column(p.lexer.lexdata, p.lexer)

    p[0] = Operation(line, column, p[2], p[1], p[3])


def p_arithmetic_operator(p):
    """arithmetic_operator : DIVIDE
                           | MINUS
                           | MOD
                           | PLUS
                           | TIMES"""
    p[0] = p[1]


def p_comparison_operator(p):
    """comparison_operator : EQ
                           | GE
                           | GT
                           | LE
                           | LT
                           | NEQ"""
    p[0] = p[1]


def p_logical_operator(p):
    """logical_operator : AND
                        | OR"""
    p[0] = p[1]


def p_native_function(p):
    """native_function : CONSOLE DOT LOG LPAREN arguments RPAREN
                       | PARSEFLOAT LPAREN expression RPAREN
                       | PARSEINT LPAREN expression RPAREN
                       | TYPEOF LPAREN expression RPAREN
                       | expression DOT TOLOWERCASE LPAREN RPAREN
                       | expression DOT TOSTRING LPAREN RPAREN
                       | expression DOT TOUPPERCASE LPAREN RPAREN"""
    if p[1] == "console" and p[2] == "." and p[3] == "log":
        line = p.lexer.lineno
        column = find_column(p.lexer.lexdata, p.lexer)

        p[0] = Print(line, column, p[5])
    elif p[1] == "parseFloat":
        p[0] = ("parse_float", p[3])
    elif p[1] == "parseInt":
        p[0] = ("parse_int", p[3])
    elif p[1] == "typeof":
        p[0] = ("type_of", p[3])
    elif p[2] == "." and p[3] == "toLowerCase":
        p[0] = ("to_lowercase", p[1])
    elif p[2] == "." and p[3] == "toString":
        p[0] = ("to_string", p[1])
    elif p[2] == "." and p[3] == "toUpperCase":
        p[0] = ("to_uppercase", p[1])


def p_primitive(p):
    """primitive : BOOLEAN
                 | CHAR
                 | FLOAT
                 | NULL
                 | NUMBER
                 | STRING"""
    p[0] = p[1]


def p_ternary_operator(p):  # Se creó una producción para el operador ternario debido a errores con la condición.
    """ternary_operator : binary_operation QUESTION expression COLON expression"""
    line = p.lexer.lineno
    column = find_column(p.lexer.lexdata, p.lexer)

    p[0] = TernaryOperator(line, column, p[1], p[3], p[5])


def p_unary_operation(p):
    """unary_operation : MINUS expression
                       | NOT expression"""
    line = p.lexer.lineno
    column = find_column(p.lexer.lexdata, p.lexer)

    p[0] = Operation(line, column, p[1], p[2], None)


def p_flow_statements(p):
    """flow_statements : for_statement
                       | if_statement
                       | switch_statement
                       | while_statement"""
    p[0] = p[1]


"""Se usó 'statement' y 'expression_statement' porque estas producciones ya incluyen el ';'."""


def p_for_statement(p):
    """for_statement : FOR LPAREN expression OF expression RPAREN statement_block
                     | FOR LPAREN statement expression_statement update RPAREN statement_block"""
    line = p.lexer.lineno
    column = find_column(p.lexer.lexdata, p.lexer)

    if p[3] == "of":  # Si el tercer elemento es 'of', entonces es un 'for-of'.
        p[0] = ("for_of", p[5], p[7])
    else:  # Si el tercer elemento no es 'of', entonces es un 'for'.
        p[0] = ForInstruction(line, column, p[3], p[4], p[5], p[7])


def p_update(p):
    """update : IDENTIFIER DECREMENT
              | IDENTIFIER INCREMENT"""
    line = p.lexer.lineno
    column = find_column(p.lexer.lexdata, p.lexer)

    if p[2] == "--":
        variable_value = VariableAccess(line, column, p[1])
        operation_result = Operation(line, column, '-', variable_value, Primitive(line, column, 1, Types.NUMBER))

        p[0] = Assignment(line, column, p[1], operation_result)
    else:
        variable_value = VariableAccess(line, column, p[1])
        operation_result = Operation(line, column, '+', variable_value, Primitive(line, column, 1, Types.NUMBER))

        p[0] = Assignment(line, column, p[1], operation_result)


def p_statement_block(p):
    """statement_block : LBRACE RBRACE
                       | LBRACE statements RBRACE"""
    if len(p) == 3:  # Si solo hay 3 elementos, es decir, 'LBRACE' 'RBRACE', entonces no hay nada en el bloque.
        p[0] = []
    else:  # Si hay más de 3 elementos, entonces hay instrucciones en el bloque.
        p[0] = p[2]


def p_if_statement(p):
    """if_statement : IF LPAREN expression RPAREN statement_block
                    | IF LPAREN expression RPAREN statement_block ELSE statement_block
                    | IF LPAREN expression RPAREN statement_block ELSE if_statement"""
    line = p.lexer.lineno
    column = find_column(p.lexer.lexdata, p.lexer)

    if len(p) == 6:  # Si solo hay 6 elementos, entonces no hay un 'else-if' o un 'else'.
        p[0] = IfInstruction(line, column, p[3], p[5])
    else:  # Si hay 8 elementos, entonces existe la posibilidad de un 'else-if' o un 'else'.
        p[0] = IfInstruction(line, column, p[3], p[5], p[7])


def p_switch_statement(p):
    """switch_statement : SWITCH LPAREN expression RPAREN LBRACE switch_cases RBRACE
                        | SWITCH LPAREN expression RPAREN LBRACE switch_cases default_case RBRACE"""
    line = p.lexer.lineno
    column = find_column(p.lexer.lexdata, p.lexer)

    if len(p) == 8:  # Si solo hay 8 elementos, entonces no hay un caso por defecto.
        p[0] = SwitchInstruction(line, column, p[3], p[6])
    else:  # Si hay 9 elementos, entonces hay un caso por defecto.
        p[0] = SwitchInstruction(line, column, p[3], p[6], p[7])


def p_switch_cases(p):
    """switch_cases : switch_case
                    | switch_cases switch_case"""
    if len(p) == 2:  # Si solo hay 2 elementos, entonces solo hay un caso.
        p[0] = [p[1]]
    else:  # Si hay más de 2 elementos, entonces hay más de un caso.
        p[0] = p[1] + [p[2]]


def p_switch_case(p):
    """switch_case : CASE expression COLON statements"""
    p[0] = (p[2], p[4])


def p_default_case(p):
    """default_case : DEFAULT COLON statements"""
    p[0] = p[3]


def p_while_statement(p):
    """while_statement : WHILE LPAREN expression RPAREN statement_block"""
    line = p.lexer.lineno
    column = find_column(p.lexer.lexdata, p.lexer)

    p[0] = WhileInstruction(line, column, p[3], p[5])


def p_function_declaration(p):
    """function_declaration : FUNCTION IDENTIFIER LPAREN parameters RPAREN COLON type statement_block"""
    p[0] = ('function_declaration', p[2], p[4], p[7], p[8])


def p_parameters(p):
    """parameters : parameter
                  | parameters COMMA parameter"""
    if len(p) == 2:  # Si solo hay 2 elementos, entonces solo hay un parámetro.
        p[0] = [p[1]]
    else:  # Si hay más de 2 elementos, entonces hay más de un parámetro.
        p[0] = p[1] + [p[3]]


def p_parameter(p):
    """parameter : IDENTIFIER COLON type"""
    p[0] = ('parameter', p[1], p[3])


def p_type(p):
    """type : ARRAY
            | BOOLEAN
            | CHAR
            | FLOAT
            | NUMBER
            | STRING"""
    p[0] = Types[p[1].upper()]  # Se debe de convertir a mayúsculas para que coincida.


def p_transfer_statement(p):
    """transfer_statement : break_statement
                          | continue_statement
                          | return_statement"""
    p[0] = p[1]


def p_break_statement(p):
    """break_statement : BREAK SEMICOLON"""
    line = p.lexer.lineno
    column = find_column(p.lexer.lexdata, p.lexer)

    p[0] = BreakStatement(line, column)


def p_continue_statement(p):
    """continue_statement : CONTINUE SEMICOLON"""
    line = p.lexer.lineno
    column = find_column(p.lexer.lexdata, p.lexer)

    p[0] = ContinueStatement(line, column)


def p_return_statement(p):
    """return_statement : RETURN expression SEMICOLON"""
    line = p.lexer.lineno
    column = find_column(p.lexer.lexdata, p.lexer)

    p[0] = ReturnStatement(line, column, p[2])


def p_variable_assignment(p):
    """variable_assignment : IDENTIFIER ASSIGN expression SEMICOLON
                           | IDENTIFIER MINUSEQUAL expression SEMICOLON
                           | IDENTIFIER PLUSEQUAL expression SEMICOLON"""
    line = p.lexer.lineno
    column = find_column(p.lexer.lexdata, p.lexer)

    if p[2] == "=":  # Si el segundo elemento es '=', entonces es una asignación normal.
        p[0] = Assignment(line, column, p[1], p[3])
    elif p[2] == "-=":  # Si el segundo elemento es '-=', entonces es una resta.
        variable_value = VariableAccess(line, column, p[1])  # Se obtiene el valor de la variable.
        operation_result = Operation(line, column, '-', variable_value, p[3])  # Se realiza la resta.

        p[0] = Assignment(line, column, p[1], operation_result)  # Se le asigna el nuevo valor a la variable.
    else:  # Si el segundo elemento es '+=', entonces es una suma.
        variable_value = VariableAccess(line, column, p[1])  # Se obtiene el valor de la variable.
        operation_result = Operation(line, column, '+', variable_value, p[3])  # Se realiza la suma.

        p[0] = Assignment(line, column, p[1], operation_result)  # Se le asigna el nuevo valor a la variable.


# noinspection DuplicatedCode
def p_variable_declaration(p):
    """variable_declaration : VAR IDENTIFIER ASSIGN expression SEMICOLON
                            | VAR IDENTIFIER COLON type ASSIGN expression SEMICOLON
                            | VAR IDENTIFIER COLON type SEMICOLON"""
    line = p.lexer.lineno
    column = find_column(p.lexer.lexdata, p.lexer)

    if len(p) == 6:  # Si hay 6 elementos, entonces no hay un tipo o un valor.
        if isinstance(p[4], Types):  # Si el cuarto elemento es un tipo, entonces no hay un valor, solo un tipo.
            default_value = Primitive(line, column, default_values.get(p[4]), p[4])  # Se obtiene el valor por defecto.

            p[0] = Declaration(line, column, p[2], p[4], default_value)
        else:  # Si el cuarto elemento no es un tipo, entonces hay un valor.
            if isinstance(p[4], Primitive):  # Al ser un primitivo, se puede obtener el tipo directamente.
                p[0] = Declaration(line, column, p[2], p[4].kind, p[4])
            else:  # Si no es un primitivo, entonces es una operación.
                left_type_value = p[4].left_operand.kind.value
                right_type_value = p[4].right_operand.kind.value

                dominant_type = Types.NULL

                if p[4].operator in {'+', '-', '*', '/', '%'}:
                    dominant_type = Operation.arithmetic_matrix[left_type_value][right_type_value]
                elif p[4].operator in {'==', '!=', '>', '>=', '<', '<='}:
                    dominant_type = Operation.relational_matrix[left_type_value][right_type_value]

                p[0] = Declaration(line, column, p[2], dominant_type, p[4])
    else:  # Si hay más de 6 elementos, entonces hay un tipo y un valor.
        if p[4] == Types.FLOAT and p[6].kind == Types.NUMBER:  # Se hace una conversión implícita de número a flotante.
            p[6].value = float(p[6].value)
            p[6].kind = Types.FLOAT

        p[0] = Declaration(line, column, p[2], p[4], p[6])


def p_error(p):
    if p:
        print(f"error de sintaxis en la línea {p.lineno}, columna {find_column(p.lexer.lexdata, p)}")
    else:
        print("error de sintaxis al final del archivo")
