import cs164interprete
from cs164interprete import eval_expression
from cs164interprete import eval_stmt
from cs164interprete import eval_block
import ply.lex as lex
import ply.yacc as yacc
import cs164lexer
import cs164parser


myLexer = lex.lex(module=cs164lexer)
myParser = yacc.yacc(debug=0, write_tables=0, module=cs164parser)


def generate_ast(input_string):
    myLexer.input(input_string)
    ast = myParser.parse(input_string, lexer=myLexer)
    return ast


def test_eval_expression():
    assert eval_block(generate_ast('1'), (None, {})) == 1
    assert eval_block(generate_ast('-1'), (None, {})) == -1
    assert eval_block(generate_ast('"done"'), (None, {})) == 'done'
    assert eval_block(generate_ast('null'), (None, {})) == 0

    assert eval_block(generate_ast('bar'), (None, {'bar': 3})) == 3
    assert eval_block(generate_ast('-bar'), (None, {'bar': 3})) == -3
    assert eval_block(generate_ast('foo'), ((None, {'foo': 1}), {'foo': 2})) == 2
    assert eval_block(generate_ast('-foo'), ((None, {'foo': 1}), {'foo': 2})) == -2
    assert eval_block(generate_ast('foo'), ((None, {'bar': 1}), {'foo': 2})) == 2
    assert eval_block(generate_ast('-foo'), ((None, {'bar': 1}), {'foo': 2})) == -2
    assert eval_block(generate_ast('foo'), ((None, {'foo': 1}), {'bar': 2})) == 1
    assert eval_block(generate_ast('-foo'), ((None, {'foo': 1}), {'bar': 2})) == -1

    assert eval_block(generate_ast('bar'), (None, {'bar': 'hello'})) == 'hello'
    assert eval_block(generate_ast('foo'), ((None, {'foo': 'hello'}), {'foo': 'hi'})) == 'hi'
    assert eval_block(generate_ast('foo'), ((None, {'bar': 'hello'}), {'foo': 'hi'})) == 'hi'
    assert eval_block(generate_ast('foo'), ((None, {'foo': 'hello'}), {'bar': 'hi'})) == 'hello'

    assert eval_block(generate_ast('1+2'), (None, {})) == 3
    assert eval_block(generate_ast('1+2+3'), (None, {})) == 6
    assert eval_block(generate_ast('1+2*3'), (None, {})) == 7
    assert eval_block(generate_ast('1*2+3'), (None, {})) == 5
    assert eval_block(generate_ast('1-2'), (None, {})) == -1
    assert eval_block(generate_ast('1-2+3'), (None, {})) == 2
    assert eval_block(generate_ast('1-2*3'), (None, {})) == -5
    assert eval_block(generate_ast('1*2-3'), (None, {})) == -1
    assert eval_block(generate_ast('1/2'), (None, {})) == 0.5
    assert eval_block(generate_ast('1/2+3'), (None, {})) == 3.5
    assert eval_block(generate_ast('1/2-3'), (None, {})) == -2.5
    assert eval_block(generate_ast('1-2/4'), (None, {})) == 0.5
    assert eval_block(generate_ast('-1+3*4/2+5-6'), (None, {})) == 4

    assert eval_block(generate_ast('fuck+shit'), (None, {'fuck': 2, 'shit': 3})) == 5
    assert eval_block(generate_ast('fuck+3'), (None, {'fuck': 2, 'shit': 3})) == 5
    assert eval_block(generate_ast('3+fuck'), (None, {'fuck': 2, 'shit': 3})) == 5
    assert eval_block(generate_ast('fuck*2'), (None, {'fuck': 2, 'shit': 3})) == 4
    assert eval_block(generate_ast('2*fuck'), (None, {'fuck': 2, 'shit': 3})) == 4
    assert eval_block(generate_ast('fuck-2'), (None, {'fuck': 2, 'shit': 3})) == 0
    assert eval_block(generate_ast('2-fuck'), (None, {'fuck': 2, 'shit': 3})) == 0
    assert eval_block(generate_ast('fuck/2'), (None, {'fuck': 2, 'shit': 3})) == 1
    assert eval_block(generate_ast('2/fuck'), (None, {'fuck': 2, 'shit': 3})) == 1
    assert eval_block(generate_ast('-fuck+shit'), (None, {'fuck': 2, 'shit': 3})) == 1
    assert eval_block(generate_ast('fuck+3*4/2-5'), (None, {'fuck': 2, 'shit': 3})) == 3
    assert eval_block(generate_ast('fuck+shit'), ((None, {'shit': 1}), {'fuck': 2})) == 3

    assert eval_block(generate_ast('1>2'), (None, {})) == 0
    assert eval_block(generate_ast('1>=2'), (None, {})) == 0
    assert eval_block(generate_ast('1<2'), (None, {})) == 1
    assert eval_block(generate_ast('1<=2'), (None, {})) == 1
    assert eval_block(generate_ast('1==2'), (None, {})) == 0
    assert eval_block(generate_ast('1!=2'), (None, {})) == 1
    assert eval_block(generate_ast('1==1'), (None, {})) == 1

    assert eval_block(generate_ast('1>2<1'), (None, {})) == 1
    assert eval_block(generate_ast('1>2>1'), (None, {})) == 0
    assert eval_block(generate_ast('1>=2<=1'), (None, {})) == 1
    assert eval_block(generate_ast('1>=2>=1'), (None, {})) == 0
    assert eval_block(generate_ast('1>2==1'), (None, {})) == 0
    assert eval_block(generate_ast('1>2!=1'), (None, {})) == 1

    assert eval_block(generate_ast('fuck>shit'), (None, {'fuck': 1, 'shit': 2})) == 0
    assert eval_block(generate_ast('fuck<shit'), (None, {'fuck': 1, 'shit': 2})) == 1
    assert eval_block(generate_ast('fuck==shit'), (None, {'fuck': 1, 'shit': 2})) == 0
    assert eval_block(generate_ast('fuck!=shit'), (None, {'fuck': 1, 'shit': 2})) == 1
    assert eval_block(generate_ast('fuck>=shit'), (None, {'fuck': 1, 'shit': 2})) == 0
    assert eval_block(generate_ast('fuck<=shit'), (None, {'fuck': 1, 'shit': 2})) == 1
    assert eval_block(generate_ast('fuck>shit'), ((None, {'shit': 1}), {'fuck': 0})) == 0

    assert eval_block(generate_ast('"fuck"=="fuck"'), (None, {})) == 1


def test_variable():
    input1 = ''' def fuck = 1
                 fuck'''
    assert eval_block(generate_ast(input1), (None, {})) == 1
    input2 = ''' def fuck = "fuck"
                 fuck'''
    assert eval_block(generate_ast(input2), (None, {})) == 'fuck'
    input3 = ''' def shit = 3
                 def fuck = shit
                 fuck'''
    assert eval_block(generate_ast(input3), (None, {})) == 3
    input4 = ''' def shit = "shit"
                 def fuck = shit
                 fuck'''
    assert eval_block(generate_ast(input4), (None, {})) == 'shit'

    input5 = ''' def fuck = 1+3
                 fuck'''
    assert eval_block(generate_ast(input5), (None, {})) == 4
    input6 = ''' def shit = 1+3*4/2-5
                 def fuck = shit
                 fuck'''
    assert eval_block(generate_ast(input6), (None, {})) == 2

    input7 = ''' def fuck = 1
                 fuck = 2
                 fuck'''
    assert eval_block(generate_ast(input7), (None, {})) == 2

    input8 = ''' def fuck = 2
                 fuck = "fuck"
                 fuck'''
    assert eval_block(generate_ast(input8), (None, {})) == 'fuck'


def test_function():
    input1 = 'def fuck(){1+2} fuck()'
    assert eval_block(generate_ast(input1), (None, {})) == 3
    input2 = ''' def fuck(){
                     1 + 2}
                 def shit = fuck()
                 shit'''
    assert eval_block(generate_ast(input2), (None, {})) == 3

    input3 = ''' def fuck(x){
                     x+2}
                 fuck(1)'''
    assert eval_block(generate_ast(input3), (None, {})) == 3
    input4 = ''' def fuck(x){
                     x*2}
                 def y = 4
                 fuck(y)'''
    assert eval_block(generate_ast(input4), (None, {})) == 8
    input5 = ''' def fuck(x, y){
                     x + y}
                 fuck(1,2)'''
    assert eval_block(generate_ast(input5), (None, {})) == 3
    input6 = ''' def fuck(x, y){
                     x * y}
                 def asshole = 100
                 def shit = 99
                 fuck(asshole, shit)'''
    assert eval_block(generate_ast(input6), (None, {})) == 9900

    input7 = ''' def x = lambda(){2}
                 x()'''
    assert eval_block(generate_ast(input7), (None, {})) == 2

    input8 = ''' def x = lambda(x){x}
                 x(2)'''
    assert eval_block(generate_ast(input8), (None, {})) == 2

    input9 = ''' def double = lambda(x) {2*x}
                 def shit(fun, n){
                     fun(n)
                 }
                 shit(double, 2)'''
    assert eval_block(generate_ast(input9), (None, {})) == 4


def test_ite():
    assert eval_block(generate_ast('ite(null, 1, 0)'), (None, {})) == 0
    assert eval_block(generate_ast('ite(1>0, "true", "false")'), (None, {})) == 'true'
    assert eval_block(generate_ast('ite(1<0, "true", "false")'), (None, {})) == 'false'
    assert eval_block(generate_ast('ite("fuck"=="fuck", 1+2+3, 3-2-1)'), (None, {})) == 6


def test_print():
    eval_block(generate_ast('print 1'), (None, {}))
    eval_block(generate_ast('print 1+1'), (None, {}))
    eval_block(generate_ast('print "holy shit"'), (None, {}))
    input1 = ''' def x = 100
                 print x'''
    eval_block(generate_ast(input1), (None, {}))


def test_ifelse():
    input1 = ''' if (1 > 0){
                     "hello"
                 } else{
                     "hi"
                 }'''
    assert eval_block(generate_ast(input1), (None, {})) == 'hello'
    input2 = ''' if (1 < 0){
                     1 +2
                 } else{
                     7*8
                 }'''
    assert eval_block(generate_ast(input2), (None, {})) == 56
    input3 = ''' def fuck(x){
                     if(x==0){
                         0
                     } else{
                         fuck(x-1) + x
                     }
                 }
                 fuck(3)'''
    assert eval_block(generate_ast(input3), (None, {})) == 6
    input4 = ''' def y = 1
                 def fac(n){
                     if(n <= 1){
                         y
                     } else{
                         n * fac(n -1)
                     }
                 }
                 fac(3)'''
    assert eval_block(generate_ast(input4), (None, {})) == 6


def test_combine():
    input1 = ''' def x = 1
                 def fuck(){
                     def x = 3
                     x
                 }
                 fuck()'''
    assert eval_block(generate_ast(input1), (None, {})) == 3
    input2 = ''' def x = 1
                 def fuck(){
                     x = 2
                 }
                 fuck()
                 x'''
    assert eval_block(generate_ast(input2), (None, {})) == 2
    input3 = ''' def x = 1
                 def fuck(){
                     x = 2
                 }
                 x'''
    assert eval_block(generate_ast(input3), (None, {})) == 1

    input4 = ''' def hello(){
                     print "hello world!"
                 }
                 hello()'''
    eval_block(generate_ast(input4), (None, {}))

    input5 = ''' def fuck(){
                     1 + 2
                 }
                 def shit(){
                     3 + fuck()
                 }
                 shit()'''
    assert eval_block(generate_ast(input5), (None, {})) == 6

    input6 = ''' def x = 2
                 x = x - 1
                 x'''
    assert eval_block(generate_ast(input6), (None, {})) == 1


def test():
    test_eval_expression()
    test_variable()
    test_function()
    test_ite()
    test_print()
    test_ifelse()
    test_combine()
    print('tests pass')


if __name__ == '__main__':
    test()


