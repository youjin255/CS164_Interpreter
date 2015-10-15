import ply.yacc as yacc
import ply.lex as lex
from cs164lexer import tokens


start = 'block'

precedence = (
    ('left', 'EQUAL'),
    ('left', 'EQUALEQUAL', 'NOTEQUAL'),
    ('left', 'LE', 'GE', 'GREATER', 'LESS'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)


def p_block(p):
    """ block : statement block"""
    p[0] = [('stmt', p[1])] + p[2]


def p_block_empty(p):
    """ block : """
    p[0] = []


def p_statement_expr(p):
    """ statement : expression"""
    p[0] = ('expr', p[1])


def p_statement_assign(p):
    """ statement : ID EQUAL expression"""
    p[0] = ('assign', p[1], p[3])


def p_statement_var_dec(p):
    """ statement : DEFINE ID EQUAL expression"""
    p[0] = ('var-dec', p[2], p[4])


def p_statement_fun_dec(p):
    """ statement : DEFINE ID LPAREN optparam RPAREN LBRACE block RBRACE"""
    p[0] = ('fun', p[2], p[4], p[7])


def p_statement_print_and_error(p):
    """ statement : PRINT expression
                  | ERROR expression"""
    p[0] = (p[1], p[2])


def p_statement_ifelse(p):
    """ statement : IF LPAREN expression RPAREN LBRACE block RBRACE ELSE LBRACE block RBRACE"""
    p[0] = ('if-else', p[3], p[6], p[10])


def p_statement_while(p):
    """ statement : WHILE LPAREN expression RPAREN LBRACE block RBRACE"""
    p[0] = ('while', p[3], p[6])


def p_statement_for(p):
    """ statement : FOR LPAREN ID IN expression RPAREN LBRACE block RBRACE"""
    p[0] = ('for', p[3], p[5], p[9])


def p_optparam(p):
    """ optparam : param"""
    p[0] = p[1]


def p_optparam_empty(p):
    """ optparam : """
    p[0] = []


def p_param_one(p):
    """ param : ID"""
    p[0] = [p[1]]


def p_param_multi(p):
    """ param : ID COMMA param"""
    p[0] = [p[1]] + p[3]


def p_expression_null(p):
    """ expression : NULL"""
    p[0] = ('null', p[1])


def p_expression_id(p):
    """ expression : ID"""
    p[0] = ('id', p[1])


def p_expression_number(p):
    """ expression : NUMBER"""
    p[0] = ('number', p[1])


def p_expression_string(p):
    """ expression : STRING"""
    p[0] = ('string', p[1])


def p_expression_operation(p):
    """ expression : expression PLUS expression
                   | expression MINUS expression
                   | expression TIMES expression
                   | expression DIVIDE expression
                   | expression EQUALEQUAL expression
                   | expression NOTEQUAL expression
                   | expression LE expression
                   | expression GE expression
                   | expression GREATER expression
                   | expression LESS expression"""
    p[0] = ('binop', p[2], p[1], p[3])


def p_expression_minus(p):
    """ expression : MINUS NUMBER
                   | MINUS ID
                   | MINUS expression"""
    p[0] = ('minus', p[2])


def p_expression_lambda(p):
    """ expression : LAMBDA LPAREN optparam RPAREN LBRACE block RBRACE"""
    p[0] = ('lambda', p[3], p[6])


def p_expression_call(p):
    """ expression : ID LPAREN optargv RPAREN"""
    p[0] = ('call', p[1], p[3])


def p_expression_ite(p):
    """ expression : ITE LPAREN expression COMMA expression COMMA expression RPAREN"""
    p[0] = ('ite', p[3], p[5], p[7])


def p_optargv(p):
    """ optargv : argv"""
    p[0] = p[1]


def p_optargv_empty(p):
    """ optargv : """
    p[0] = []


def p_argv_one(p):
    """ argv : expression"""
    p[0] = [p[1]]


def p_argv_multi(p):
    """ argv : expression COMMA argv"""
    p[0] = [p[1]] + p[3]


def p_error(p):
    print("Syntax error at token", p.type)
    # Just discard the token and tell the parser it's okay.
    yacc.errok()
