# coding: utf-8

__author__ = "Korantin"


import ply.lex as lex

literals = '()'

tokens = (
    'SYNTAGME',
    'MOT'
)

def t_SYNTAGME(t):
    r'[A-Z\+\-][A-Z\+\-]*'
    return t

def t_MOT(t):
    r'[A-Za-z1-9-_+][A-Za-z]*'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' '

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex(optimize=1,lextab="gloseur")

data = '( SENT MOT)'

lexer.input(data)


while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)