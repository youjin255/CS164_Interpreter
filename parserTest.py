import ply.lex as lex
import ply.yacc as yacc
import cs164lexer
import cs164parser


myLexer = lex.lex(module=cs164lexer)
myParser = yacc.yacc(debug=0, write_tables=0, module=cs164parser)


def test_parser(input_string):
    myLexer.input(input_string)
    ast = myParser.parse(input_string, lexer=myLexer)
    return ast


def test_expression_string():
    assert test_parser('"holy shit"') == [('stmt', ('expr', ('string', 'holy shit')))]
    assert test_parser("'author loucq'") == [('stmt', ('expr', ('string', 'author loucq')))]


def test_expression_number():
    assert test_parser('1') == [('stmt', ('expr', ('number', 1)))]
    assert test_parser('-1') == [('stmt', ('expr', ('minus', ('number', 1))))]
    assert test_parser('0') == [('stmt', ('expr', ('number', 0)))]
    assert test_parser('1234567890') == [('stmt', ('expr', ('number', 1234567890)))]
    assert test_parser('-1234567890') == [('stmt', ('expr', ('minus', ('number', 1234567890))))]


def test_expression_id():
    assert test_parser('x') == [('stmt', ('expr', ('id', 'x')))]
    assert test_parser('_') == [('stmt', ('expr', ('id', '_')))]
    assert test_parser('__') == [('stmt', ('expr', ('id', '__')))]
    assert test_parser('abc') == [('stmt', ('expr', ('id', 'abc')))]

    assert test_parser('_cba') == [('stmt', ('expr', ('id', '_cba')))]
    assert test_parser('iem9') == [('stmt', ('expr', ('id', 'iem9')))]
    assert test_parser('_2') == [('stmt', ('expr', ('id', '_2')))]

    assert test_parser('_c4') == [('stmt', ('expr', ('id', '_c4')))]
    assert test_parser('_4c') == [('stmt', ('expr', ('id', '_4c')))]

    assert test_parser('c_4') == [('stmt', ('expr', ('id', 'c_4')))]
    assert test_parser('c4_') == [('stmt', ('expr', ('id', 'c4_')))]


def test_expression_null():
    assert test_parser('null') == [('stmt', ('expr', ('null', 'null')))]


def test_expression_operation():
    assert test_parser('1+2') == [('stmt', ('expr', ('binop', '+', ('number', 1), ('number', 2))))]
    assert test_parser('1-2') == [('stmt', ('expr', ('binop', '-', ('number', 1), ('number', 2))))]
    assert test_parser('1*2') == [('stmt', ('expr', ('binop', '*', ('number', 1), ('number', 2))))]
    assert test_parser('1/2') == [('stmt', ('expr', ('binop', '/', ('number', 1), ('number', 2))))]
    assert test_parser('1>=2') == [('stmt', ('expr', ('binop', '>=', ('number', 1), ('number', 2))))]
    assert test_parser('1<=2') == [('stmt', ('expr', ('binop', '<=', ('number', 1), ('number', 2))))]
    assert test_parser('1>2') == [('stmt', ('expr', ('binop', '>', ('number', 1), ('number', 2))))]
    assert test_parser('1<2') == [('stmt', ('expr', ('binop', '<', ('number', 1), ('number', 2))))]
    assert test_parser('1==2') == [('stmt', ('expr', ('binop', '==', ('number', 1), ('number', 2))))]
    assert test_parser('1!=2') == [('stmt', ('expr', ('binop', '!=', ('number', 1), ('number', 2))))]

    # Test precedence
    assert test_parser('1+2*3') == [('stmt', ('expr', ('binop', '+', ('number', 1),
                                                           ('binop', '*', ('number', 2), ('number', 3)))))]
    assert test_parser('1*2+3') == [('stmt', ('expr', ('binop', '+',
                                                         ('binop', '*', ('number', 1), ('number', 2)),
                                                         ('number', 3))))]
    assert test_parser('1-2+3') == [('stmt', ('expr', ('binop', '+',
                                                           ('binop', '-', ('number', 1), ('number', 2)),
                                                           ('number', 3))))]


def test_expression_lambda():
    assert test_parser('lambda(){}') == [('stmt', ('expr', ('lambda', [], [])))]
    assert test_parser('lambda(x){}') == [('stmt', ('expr', ('lambda', ['x'], [])))]
    assert test_parser('lambda(){1}') == [('stmt', ('expr', ('lambda', [], [('stmt', ('expr', ('number', 1)))])))]
    assert test_parser('lambda(){x}') == [('stmt', ('expr', ('lambda', [], [('stmt', ('expr', ('id', 'x')))])))]
    assert test_parser('lambda(){1+x y}') == [('stmt', ('expr', ('lambda', [],
                                                                 [('stmt', ('expr', ('binop', '+', ('number', 1),
                                                                                     ('id', 'x')))),
                                                                  ('stmt', ('expr', ('id', 'y')))])))]
    assert test_parser('lambda(x, y){}') == [('stmt', ('expr', ('lambda', ['x', 'y'], [])))]


def test_expression_ite():
    assert test_parser('ite(1, 1, 0)') == [('stmt', ('expr', ('ite', ('number', 1), ('number', 1), ('number', 0))))]
    assert test_parser('ite(1>0, 1+2, 3*4)') == [('stmt', ('expr', ('ite',
                                                                    ('binop', '>', ('number', 1), ('number', 0)),
                                                                    ('binop', '+', ('number', 1), ('number', 2)),
                                                                    ('binop', '*', ('number', 3), ('number', 4)))))]
    assert test_parser('ite(null, lambda(){}, x)') == [('stmt', ('expr', ('ite',
                                                                         ('null', 'null'),
                                                                         ('lambda', [], []),
                                                                         ('id', 'x'))))]
    assert test_parser('ite(-1, "fuck", x)') == [('stmt', ('expr', ('ite',
                                                                    ('minus', ('number', 1)),
                                                                    ('string', 'fuck'),
                                                                    ('id', 'x'))))]


def test_stmt_ifelse():
    assert test_parser('if(1){1+1}else{"hello"}') == [('stmt', ('if-else', ('number', 1),
                                                                [('stmt', ('expr', ('binop', '+',
                                                                                    ('number', 1), ('number', 1))))],
                                                                [('stmt', ('expr', ('string', 'hello')))]))]



def test_expression():
    test_expression_string()
    test_expression_number()
    test_expression_id()
    test_expression_null()
    test_expression_operation()
    test_expression_lambda()
    test_expression_ite()


def test_statement():
    test_stmt_ifelse()


def test_block():
    pass


def test():
    test_expression()
    test_statement()
    test_block()
    print("tests pass.")

if __name__ == '__main__':
    test()