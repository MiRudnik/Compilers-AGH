import lab1.scanner as scanner
import ply.yacc as yacc
import sys
sys.path.append("..")

tokens = scanner.tokens

precedence = (
    ("nonassoc", 'GE', 'LE', 'EQ', 'NEQ', '<', '>'),
    ("left", 'M_ADD', 'M_SUB', '+', '-'),
    ("left", 'M_MUL', 'M_DIV', '*', '/'),
    ("right", 'U_MINUS'),
    ("left", 'TRANSPOSE')
)


def p_error(p):
    if p:
        print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, scanner.find_column(p),
                                                                                  p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    '''program : instructions_opt '''


def p_instructions_opt_1(p):
    '''instructions_opt : instructions '''


def p_instructions_opt_2(p):
    '''instructions_opt : '''


def p_instructions_1(p):
    '''instructions : instructions instruction ';' '''


def p_instructions_2(p):
    '''instructions : instruction ';' '''


def p_instruction_assign(p):
    '''instruction : ID '=' expression
                  | ID A_ADD expression
                  | ID A_SUB expression
                  | ID A_MUL expression
                  | ID A_DIV expression '''


def p_instruction_functions(p):
    '''expression : ZEROS '(' INT ')'
                   | ONES '(' INT ')'
                   | EYE '(' INT ')' '''


def p_instruction_relop(p):
    '''instruction : expression GE expression
                  | expression LE expression
                  | expression EQ expression
                  | expression NEQ expression
                  | expression '>' expression
                  | expression '<' expression '''


def p_instruction_bin(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression M_ADD expression
                  | expression M_SUB expression
                  | expression M_MUL expression
                  | expression M_DIV expression '''


def p_expr_transpose(p):
    '''expression : expression TRANSPOSE '''


def p_expr_uminus(p):
    '''expression : - expression %prec U_MINUS '''


def p_expression(p):
    '''expression : number
                  | ID '''


def p_number(p):
    '''number : INT
              | FLOAT '''


parser = yacc.yacc()
