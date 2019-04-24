import lab1.scanner as scanner
import lab3.AST as AST
import ply.yacc as yacc
import sys
sys.path.append("..")

tokens = scanner.tokens

has_errors = False

precedence = (
    ("left", 'IF'),
    ("left", 'ELSE'),
    ("nonassoc", 'GE', 'LE', 'EQ', 'NEQ', '<', '>'),
    ("left", 'M_ADD', 'M_SUB', '+', '-'),
    ("left", 'M_MUL', 'M_DIV', '*', '/'),
    ("right", 'U_MINUS'),
    ("left", 'TRANSPOSE')
)


def p_error(p):
    global has_errors
    has_errors = True
    if p:
        print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, scanner.find_column(p),
                                                                                  p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    '''program : instructions
               | '''
    if len(p) == 2:
        p[0] = AST.Program(p[1])
    else:
        p[0] = AST.Program()


def p_instructions(p):
    '''instructions : instructions instruction
                    | instruction '''
    if len(p) == 2:
        p[0] = AST.Instructions([p[1]])
    else:
        p[0] = p[1]
        p[0].addInstruction(p[2])


def p_instruction(p):
    '''instruction : instruction_set
                   | instruction_if
                   | instruction_assign
                   | instruction_print
                   | instruction_while
                   | instruction_for
                   | instruction_break
                   | instruction_continue
                   | instruction_return '''
    p[0] = p[1]


def p_instruction_set(p):
    '''instruction_set : '{' instructions '}' '''
    p[0] = p[2]


def p_instruction_if(p):
    '''instruction_if : IF '(' assignable ')' instruction %prec IF
                      | IF '(' assignable ')' instruction ELSE instruction '''
    if len(p) == 8:
        p[0] = AST.If(p[3], p[5], p.lineno(1), p[7])
    else:
        p[0] = AST.If(p[3], p[5], p.lineno(1))


def p_instruction_while(p):
    '''instruction_while : WHILE '(' assignable ')' instruction '''
    p[0] = AST.While(p[3], p[5], p.lineno(1))


def p_instruction_for(p):
    '''instruction_for : FOR ID '=' range instruction '''
    p[0] = AST.For(AST.Variable(p[2], p.lineno(1)), p[4], p[5], p.lineno(1))


def p_instruction_assign(p):
    '''instruction_assign : ID '=' assignable ';'
                          | ID A_ADD assignable ';'
                          | ID A_SUB assignable ';'
                          | ID A_MUL assignable ';'
                          | ID A_DIV assignable ';' '''
    p[0] = AST.Assign(p[2], AST.Variable(p[1], p.lineno(1)), p[3], p.lineno(1))


def p_instruction_assign_array_element(p):
    '''instruction_assign : ref '=' assignable ';'
                          | ref A_ADD assignable ';'
                          | ref A_SUB assignable ';'
                          | ref A_MUL assignable ';'
                          | ref A_DIV assignable ';' '''
    p[0] = AST.Assign(p[2], p[1], p[3], p.lineno(1))


def p_instruction_print(p):
    '''instruction_print : PRINT args ';' '''
    p[0] = AST.Print(p[2], p.lineno(1))


def p_instruction_break(p):
    '''instruction_break : BREAK ';' '''
    p[0] = AST.Break(p.lineno(1))


def p_instruction_continue(p):
    '''instruction_continue : CONTINUE ';' '''
    p[0] = AST.Continue(p.lineno(1))


def p_instruction_return(p):
    '''instruction_return : RETURN assignable ';'
                          | RETURN ';' '''
    if len(p) == 4:
        p[0] = AST.Return(p.lineno(1), p[2])
    else:
        p[0] = AST.Return(p.lineno(1))


def p_args(p):
    '''args : args ',' assignable
            | assignable '''
    if len(p) == 2:
        p[0] = AST.Args([p[1]])
    else:
        p[0] = p[1]
        p[0].addArg(p[3])


def p_range(p):
    '''range : expression ':' expression '''
    p[0] = AST.Range(p[1], p[3], p.lineno(1))


def p_assignable(p):
    '''assignable : relop
                  | expression
                  | vector
                  | matrix '''
    p[0] = p[1]


def p_relop(p):
    '''relop : expression GE expression
             | expression LE expression
             | expression EQ expression
             | expression NEQ expression
             | expression '>' expression
             | expression '<' expression '''
    p[0] = AST.RelExpr(p[2], p[1], p[3], p.lineno(1))


def p_matrix_functions(p):
    '''expression : ZEROS '(' expr_list ')'
                  | ONES '(' expr_list ')'
                  | EYE '(' expr_list ')' '''
    p[0] = AST.MatrixFunc(p[1], p[3], p.lineno(1))


def p_reference(p):
    '''ref : ID '[' expr_list ']' '''
    p[0] = AST.Ref(AST.Variable(p[1], p.lineno(1)), p[3], p.lineno(1))


def p_expr_list(p):
    '''expr_list : expr_list ',' expression
                 | expression '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]
        p[0].append(p[3])


def p_matrix(p):
    '''matrix :  '[' matrix_values ']' '''
    p[0] = p[2]


def p_matrix_values(p):
    '''matrix_values : vector
                     | vector ',' matrix_values '''
    if len(p) == 2:
        p[0] = AST.Vector([p[1]], p.lineno(1))
    else:
        p[0] = p[3]
        p[0].addValue(p[1])


def p_vector_1(p):
    '''vector :  '[' vector_values ']' '''
    p[0] = p[2]


def p_vector_values(p):
    '''vector_values : const
                     | const ',' vector_values '''
    if len(p) == 2:
        p[0] = AST.Vector([p[1]], p.lineno(1))
    else:
        p[0] = p[3]
        p[0].addValue(p[1])


def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression M_ADD expression
                  | expression M_SUB expression
                  | expression M_MUL expression
                  | expression M_DIV expression '''
    p[0] = AST.BinExpr(p[2], p[1], p[3], p.lineno(2))


def p_expr_transpose(p):
    '''expression : ID TRANSPOSE '''
    p[0] = AST.Transpose(AST.Variable(p[1], p.lineno(1)), p.lineno(2))


def p_expr_uminus(p):
    '''expression : - expression %prec U_MINUS '''
    p[0] = AST.UMinus(p[2], p.lineno(1))


def p_expression_1(p):
    '''expression : const '''
    p[0] = p[1]


def p_expression_2(p):
    '''expression : ID '''
    p[0] = AST.Variable(p[1], p.lineno(1))


def p_expression_3(p):
    '''expression : ref '''
    p[0] = p[1]


def p_const_1(p):
    '''const : STRING '''
    p[0] = AST.String(p[1], p.lineno(1))


def p_const_2(p):
    '''const : INT '''
    p[0] = AST.IntNum(p[1], p.lineno(1))


def p_const_3(p):
    '''const : FLOAT '''
    p[0] = AST.FloatNum(p[1], p.lineno(1))


parser = yacc.yacc()
