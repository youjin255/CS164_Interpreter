import ply.lex as lex


states = (
    ('comment', 'exclusive'),
)


def t_comment(t):
    r'\/\*[^(?:/\\*)]*'
    t.lexer.begin('comment')


def t_comment_newline(t):
    r'\n'
    t.lexer.lineno += 1


def t_comment_error(t):
    print("Illeagel character in comment '%s'" % t.value[0])
    t.lexer.skip(1)


def t_comment_end(t):
    r'\*\/'
    t.lexer.begin('INITIAL')


reserved = {
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "for": "FOR",
    "def": "DEFINE",
    "print": "PRINT",
    "error": "ERROR",
    "null": "NULL",
    "ite": "ITE",
    'in': 'IN',
    'lambda': 'LAMBDA',
}

tokens = [
    "NUMBER",
    "ID",
    "STRING",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "EQUALEQUAL",
    "EQUAL",
    "NOTEQUAL",
    "LE",
    "GE",
    "GREATER",
    "LESS",
    "LPAREN",
    "RPAREN",
    "LBRACE",
    "RBRACE",
    "COMMA",
] + list(reserved.values())


def t_NUMBER(t):
    r'([1-9][0-9]*)|0'
    t.value = int(t.value)
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_STRING(t):
    r"\"[^\"]*\"|'[^']*'"
    t.value = t.value[1: -1]
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUAL = r'='
t_EQUALEQUAL = r'=='

t_NOTEQUAL = r'!='
t_LE = r'<='
t_GE = r'>='
t_GREATER = r'>'
t_LESS = r'<'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_COMMA = r','

t_ignore = ' \t\v\r'
t_comment_ignore = ' \t\v\r'












