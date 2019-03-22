import lab1.scanner as scanner
import ply.yacc as yacc

tokens = scanner.tokens

precedence = (
    ("nonassoc", 'GE', 'LE', 'EQ', 'NEQ', '<', '>'),
    ("left", 'M_ADD', 'M_SUB', '+', '-'),
    ("left", 'M_MUL', 'M_DIV', '*', '/'),
    ("right", 'U_MINUS'),
    ("left", 'TRANSPOSE')
)

symtab = {}


def p_error(p):
    if p:
        print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, scanner.find_tok_column(p),
                                                                                  p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    """program : instructions_opt"""


def p_expression(p):
    '''expression : INT
                  | FLOAT
                  | STRING'''
    p[0] = p[1]


def p_expression_var(p):
    """expression : ID"""
    val = symtab.get(p[1])
    if val:
        p[0] = val
    else:
        p[0] = 0
        print("%s not used\n" %p[1])


def p_expression_assign(t):
    '''expression : ID '=' expression
                  | ID A_ADD expression
                  | ID A_SUB expression
                  | ID A_MUL expression
                  | ID A_DIV expression'''
    if t[2] == '=':
        t[0] = t[3]

    elif t[2] == 'A_ADD' : t[0] = t[1] + t[3]


def p_expression_binop(t):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression M_ADD expression
                  | expression M_SUB expression
                  | expression M_MUL expression
                  | expression M_DIV expression'''
    if t[2] == '+'  : t[0] = t[1] + t[3]
    elif t[2] == '-': t[0] = t[1] - t[3]
    elif t[2] == '*': t[0] = t[1] * t[3]
    elif t[2] == '/': t[0] = t[1] / t[3]
    elif t[2] == 'M_ADD': t[0] = t[1] + t[3]
    elif t[2] == 'M_SUB': t[0] = t[1] - t[3]
    elif t[2] == 'M_MUL': t[0] = t[1] * t[3]
    elif t[2] == 'M_DIV': t[0] = t[1] / t[3]


def p_expression_relop(t):
    '''expression : expression GE expression
                  | expression LE expression
                  | expression EQ expression
                  | expression NEQ expression
                  | expression '>' expression
                  | expression '<' expression'''
    if t[2] == 'GE'  : t[0] = t[1] >= t[3]
    elif t[2] == 'LE': t[0] = t[1] <= t[3]
    elif t[2] == 'EQ': t[0] = t[1] == t[3]
    elif t[2] == 'NEQ': t[0] = t[1] != t[3]
    elif t[2] == '>': t[0] = t[1] > t[3]
    elif t[2] == '<': t[0] = t[1] < t[3]


def p_expr_uminus(p):
    'expression : - expression %prec U_MINUS'
    p[0] = -p[2]


def p_expr_transpose(p):
    'expression : \' expression %prec TRANSPOSE'
    p[0] = p[2]


parser = yacc.yacc()
