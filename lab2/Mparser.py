import lab1.scanner as scanner
import lab3.AST as AST
import ply.yacc as yacc
import sys
sys.path.append("..")

tokens = scanner.tokens

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
    p[0] = AST.InstructionSet(p[2])


def p_instruction_if(p):
    '''instruction_if : IF '(' assignable ')' instruction %prec IF
                      | IF '(' assignable ')' instruction ELSE instruction '''
    if len(p) == 8:
        p[0] = AST.If(p[3], p[5], p[7])
    else:
        p[0] = AST.If(p[3], p[5])


def p_instruction_while(p):
    '''instruction_while : WHILE '(' assignable ')' instruction '''
    p[0] = AST.While(p[3], p[5])


def p_instruction_for(p):
    '''instruction_for : FOR ID '=' range instruction '''
    p[0] = AST.For(p[2], p[4], p[5])


def p_instruction_assign(p):
    '''instruction_assign : ID '=' assignable ';'
                          | ID A_ADD assignable ';'
                          | ID A_SUB assignable ';'
                          | ID A_MUL assignable ';'
                          | ID A_DIV assignable ';' '''
    p[0] = AST.Assign(p[2], p[1], p[3])


def p_instruction_assign_array_element(p):
    '''instruction_assign : ID '[' INT ',' INT ']' '=' assignable ';'
                          | ID '[' INT ',' INT ']' A_ADD assignable ';'
                          | ID '[' INT ',' INT ']' A_SUB assignable ';'
                          | ID '[' INT ',' INT ']' A_MUL assignable ';'
                          | ID '[' INT ',' INT ']' A_DIV assignable ';' '''
    p[0] = AST.Assign(p[7], AST.Ref(p[1], p[3], p[5]), p[8])


def p_instruction_print(p):
    '''instruction_print : PRINT args ';' '''
    p[0] = AST.Print(p[2])


def p_instruction_break(p):
    '''instruction_break : BREAK ';' '''
    p[0] = AST.Break()


def p_instruction_continue(p):
    '''instruction_continue : CONTINUE ';' '''
    p[0] = AST.Continue()


def p_instruction_return(p):
    '''instruction_return : RETURN assignable ';'
                          | RETURN ';' '''
    if len(p) == 4:
        p[0] = AST.Return(p[2])
    else:
        p[0] = AST.Return('')


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
    p[0] = AST.Range(p[1], p[3])


def p_assignable(p):
    '''assignable : relop
                  | expression
                  | STRING
                  | array '''
    p[0] = p[1]


def p_relop(p):
    '''relop : expression GE expression
             | expression LE expression
             | expression EQ expression
             | expression NEQ expression
             | expression '>' expression
             | expression '<' expression '''
    p[0] = AST.RelExpr(p[2], p[1], p[3])


def p_matrix_functions(p):
    '''expression : ZEROS '(' INT ')'
                  | ONES '(' INT ')'
                  | EYE '(' INT ')' '''
    p[0] = AST.MatrixFunc(p[1], p[3])


def p_array(p):
    '''array :  '[' rows ']'
             | '[' ']' '''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = AST.Values([])


def p_rows(p):
    '''rows : values
           | values ';' rows
           | array
           | array ',' rows '''
    if len(p) == 2:
        p[0] = AST.Values([p[1]])
    else:
        p[0] = p[3]
        p[0].addValue(p[1])


def p_values(p):
    '''values : value
              | value ',' values '''
    if len(p) == 2:
        p[0] = AST.Values([p[1]])
    else:
        p[0] = p[3]
        p[0].addValue(p[1])


def p_value(p):
    '''value : number
             | STRING '''
    p[0] = p[1]


def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression M_ADD expression
                  | expression M_SUB expression
                  | expression M_MUL expression
                  | expression M_DIV expression '''
    p[0] = AST.BinExpr(p[2], p[1], p[3])


def p_expr_transpose(p):
    '''expression : ID TRANSPOSE '''
    p[0] = AST.Transpose(p[1])


def p_expr_uminus(p):
    '''expression : - expression %prec U_MINUS '''
    p[0] = AST.UMinus(p[2])


def p_expression(p):
    '''expression : number
                  | ID '''
    p[0] = p[1]


def p_number(p):
    '''number : INT '''
    p[0] = AST.IntNum(p[1])


def p_float(p):
    '''number : FLOAT '''
    p[0] = AST.FloatNum(p[1])


parser = yacc.yacc()
