import ply.lex as lex
import cs164lexer


myLexer = lex.lex(module=cs164lexer)


def test_lexer(input_string):
    myLexer.input(input_string)
    result = []
    while True:
        tok = myLexer.token()
        if not tok:
            break
        result = result + [(tok.type, tok.value)]
    return result


def test_lexer_single_token():
    single_tokens = '''if else while for def print error null ite
                     + - * / == = != <= >= < > ( ) , { } in lambda'''
    single_token_types = [('IF', 'if'), ('ELSE', 'else'), ('WHILE', 'while'), ('FOR', 'for'),
                          ('DEFINE', 'def'), ('PRINT', 'print'), ('ERROR', 'error'), ('NULL', 'null'),
                          ('ITE', 'ite'), ('PLUS', '+'), ('MINUS', '-'), ('TIMES', '*'), ('DIVIDE', '/'),
                          ('EQUALEQUAL', '=='), ('EQUAL', '='), ('NOTEQUAL', '!='), ('LE', '<='), ('GE', '>='),
                          ('LESS', '<'), ('GREATER', '>'), ('LPAREN', '('), ('RPAREN', ')'), ('COMMA', ','),
                          ('LBRACE', '{'), ('RBRACE', '}'), ('IN', 'in'), ('LAMBDA', 'lambda')]
    assert test_lexer(single_tokens) == single_token_types


def test_lexer_number():
    numbers = '0 -1 1 1234567890 -1234567890'
    numbers_types = [('NUMBER', 0), ('NUMBER', -1), ('NUMBER', 1),
                     ('NUMBER', 1234567890), ('NUMBER', -1234567890)]
    assert test_lexer(numbers) == numbers_types


def test_lexer_string():
    strings = '"fuck" "shit" "f" "s" "1" "123" "_+" "-+123" "123lou" "lou_+"'
    strings_types = [('STRING', 'fuck'), ('STRING', 'shit'), ('STRING', 'f'), ('STRING', 's'),
                     ('STRING', '1'), ('STRING', '123'), ('STRING', '_+'), ('STRING', '-+123'),
                     ('STRING', '123lou'), ('STRING', 'lou_+')]
    assert test_lexer(strings) == strings_types


def test_lexer_comment():
    assert test_lexer('/* hello */') == []
    assert test_lexer('/**/') == []
    assert test_lexer('/* \n */') == []


def test_lexer_combine():
    test_case = '''if "sith dnatsrednu nac uoy" /* you must get bored */
                   else 'is' 3 + 4 = 7 '?' /* you got it! Clever boy\n */
                '''
    test_answer = [('IF', 'if'), ('STRING', 'sith dnatsrednu nac uoy'), ('ELSE', 'else'),
                   ('STRING', 'is'), ('NUMBER', 3), ('PLUS', '+'), ('NUMBER', 4), ('EQUAL', '='),
                   ('NUMBER', 7), ('STRING', '?')]
    assert test_lexer(test_case) == test_answer


def test():
    test_lexer_single_token()
    test_lexer_number()
    test_lexer_string()
    test_lexer_comment()
    test_lexer_combine()
    print("Tests pass.")


if __name__ == '__main__':
    test()




