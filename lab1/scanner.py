import ply.lex as lex

literals = ['+', '-', '*', '/', '(', ')', '[', ']', '{', '}', '<', '>', '\'', ':', ',', ';', '=']

tokens = ('M_ADD', 'M_SUB', 'M_MUL', 'M_DIV', 'A_ADD', 'A_SUB', 'A_MUL', 'A_DIV', 'GE', 'LE', 'EQ', 'NEQ', 'IF', 'FOR',
          'ELSE', 'WHILE', 'BREAK', 'RETURN', 'CONTINUE', 'EYE', 'ZEROS', 'ONES', 'PRINT', 'ID', 'FLOAT', 'INT',
          'STRING', 'COMMENT')

reserved = ['if', 'then', 'else', 'while', 'break', 'return', 'continue', 'eye', 'zeros', 'ones', 'print']

t_M_ADD = r'\.\+'
t_M_SUB = r'\.-'
t_M_MUL = r'\.\*'
t_M_DIV = r'\./'

t_A_ADD = r'\+='
t_A_SUB = r'-='
t_A_MUL = r'\*='
t_A_DIV = r'/='

t_GE = r'>='
t_LE = r'<='
t_EQ = r'=='
t_NEQ = r'!='


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = t.value.upper() if t.value in reserved else 'ID'  # Check for reserved words
    return t


def t_FLOAT(t):
    r'[+-]?\d*((\d\.|\.\d)\d*([Ee][+-]?\d+)?|\d([Ee][+-]?\d+))'
    t.value = float(t.value)
    return t


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING(t):
    r'"([^"\\]|\\.)*" | \'([^\'\\]|\\.)*\''
    return t


t_ignore = '  \t'
t_ignore_COMMENT = r'\#.*'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
