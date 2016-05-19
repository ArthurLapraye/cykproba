#!/usr/bin/python
# coding: utf-8


import codecs
import ply.lex as lex
import ply.yacc as yacc
import yaml
from phrases import Phrase
from Nonterminal import Nonterminal
from Terminal import Terminal
from productions import *


#################### PARTIE LEXICALE ####################################

literals = '()'

tokens = ('MOT',)


def t_MOT(t):
    r'[\µ\©\#\±\°\á\Î\É\ÀA-Za-z0-9\ó\-\_\+\à\â\ä\é\è\ê\ë\î\ï\ô\ö\ù\ü\û\ç\'\.\,\:\;\/\"\ß\?\%\<\>\=\[\]\&\!\^\$\½][\©\µ\#\½\±\°\ó\á\Î\$\!\^\&\É\ÀA-Za-z0-9\-\_\+\'\.\,\à\â\ä\é\è\ê\ë\î\ï\ô\ö\ù\ü\û\ç\:\;\/\"ß\?\%\<\>\=\[\]]*'
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore = ' '


def t_error(t):
    print("Illegal character {0}".format(t.value[0]))
    t.lexer.skip(1)

lex.lex(
    optimize=1,
    lextab="lexique"
)


########################################################################

phrase = []


#################### PARTIE SYNTAXIQUE ####################################

def p_axiome(p):
    """Sprim : '(' S ')'"""
    p[0] = p[2][0]


def p_S_1(p):
    """S : '(' syntagme ')'"""
    p[0] = p[2]


def p_S_2(p):
    """ S : '(' lexique ')' """
    p[0] = p[2]


def p_syntagme(p):
    """ syntagme : head exprs """
    rhs = [x[0] for x in p[2]]
    if len(rhs) == 1:
        Productionhorscontexteprobabiliseeunaire((p[1],), rhs)
    elif len(p[2]) == 2:
        Productionhorscontexteprobabiliseebinaire((p[1],), rhs)
    else:
        Productionhorscontexteprobabiliseenaire((p[1],), rhs)
    p[0] = [[p[1], p[2]]]


def p_exprs(p):
    """ exprs : S exprs
              | S
    """
    if len(p) == 3:
        p[1].extend(p[2])
        p[0] = p[1]
    else:
        p[0] = p[1]


def p_lexique(p):
    """ lexique : head leaf """
    # p[0] = [Production(lhs=p[1], rhs=p[2])]
    # p[] = [{p[1]: p[1].lower()}]
    #phrase.append(p[1].lower())
    Productionhorscontexteprobabiliseelexicale((p[1],), (p[2],))
    p[0] = [[p[1], p[2]]]


def p_head(p):
    """ head : MOT """
    p[0] = Nonterminal(p[1].split('-')[0])


def p_leaf(p):
    """ leaf : MOT """
    p[0] = Terminal(p[1])


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()


def main():
    with codecs.open("corpus/sequoia-corpus+fct.id_mrg") as id_mrg:
        phrases = []
        for ligne in id_mrg:
            (nomcorpus_numerophrase, phras) = ligne.split("\t")
            phrases.append(phras.strip())

    for (i, p) in enumerate(phrases[:2]):
        print(p)
        result = parser.parse(p)
    Productionhorscontexteprobabilisee.setprobaproductions()




        #print(result)
        # print(yaml.dump(result, default_flow_style=False, allow_unicode=True))
    # parser phrases
    # instancier PCFG

########################################################################
if __name__ == '__main__':
    main()
