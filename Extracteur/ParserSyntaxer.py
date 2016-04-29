# coding: utf-8

import ParserLexer
import codecs
#from Terminal import Terminal
#from Nonterminal import Nonterminal
#from Production import Production
import ply.yacc as yacc
import yaml

tokens = ParserLexer.tokens

# alphabet terminal représente dans une grammaire formelle, les états finaux
terminals = {}
counter_term = {}
# alphabet non-terminal représente dans une grammaire formelle soit un ou plusieurs état initiaux ou intermédiaires
non_terminals = {}
counter_nonterm = {}
# #

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
    # p[0] = [Production(lhs=p[1], rhs=[x.lhs for x in p[2]])]
    p[0] = [{p[1]: [p[2]]}]


def p_exprs(p):
    """ exprs : S exprs
              | S
    """
    if len(p) == 3:
        p[0] = p[1]+p[2]
    else:
        p[0] = p[1]


def p_lexique(p):
    """ lexique : head leaf """
    # p[0] = [Production(lhs=p[1], rhs=p[2])]
    p[0] = [{p[1]: p[2]}]


def p_head(p):
    """ head : MOT """
    # p[0] = Nonterminal(p[1])
    p[0] = p[1]


def p_leaf(p):
    """ leaf : MOT """
    # p[0] = Terminal(p[1])
    p[0] = p[1]


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

with codecs.open("../Corpus/sequoia-corpus+fct.id_mrg") as id_mrg:
    phrases = []
    for ligne in id_mrg:
        (nomcorpus_numerophrase, phrase) = ligne.split("\t")
        phrases.append(phrase.strip())

for phrase in phrases[:10]:
    result = parser.parse(phrase)
    print(yaml.dump(result,default_flow_style=False, allow_unicode=True))
