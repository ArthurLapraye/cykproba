# coding: utf-8

__author__ = "Korantin"


import ply.lex as lex

literals = '()'

tokens = (
    'MOT',
)

def t_MOT(t):
    r'[\µ\©\#\±\°\á\Î\É\ÀA-Za-z0-9\ó\-\_\+\à\â\ä\é\è\ê\ë\î\ï\ô\ö\ù\ü\û\ç\'\.\,\:\;\/\"\ß\?\%\<\>\=\[\]\&\!\^\$\½][\©\µ\#\½\±\°\ó\á\Î\$\!\^\&\É\ÀA-Za-z0-9\-\_\+\'\.\,\à\â\ä\é\è\ê\ë\î\ï\ô\ö\ù\ü\û\ç\:\;\/\"ß\?\%\<\>\=\[\]]*'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' '

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lex.lex(optimize=1,lextab="gloseur")

#data = '(SENT-SUJ (MOT CATASTROPHé))'

#lexer.input(data)


#while True:
#    tok = lexer.token()
#    if not tok:
#        break      # No more input
#    print(tok)