# coding: utf-8

import ParserLexer
tokens = ParserLexer.tokens

from Node import Node
import ply.yacc as yacc


def p_expr_1(p):
    """expr : '(' expr ')'"""
    p[0] = Node(
        head=p[2].head,
        children=[p[1]]
    )
def p_expr_2(p):
	"""expr : SYNTAGME expr"""
	p[0] = Node(
		head=p[1],
		children=[p[2]],
	)

def p_expr_3(p):
	"""expr : SYNTAGME MOT"""
	p[0] = Node(
		head=p[1],
		children=[],
		leaf=p[2]
	)

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

#with codecs.open("Ressources/sequoia-corpus+fct.id_mrg") as id_mrg:
#    phrases = []
#    for ligne in id_mrg:
#        (nomcorpus_numerophrase, phrase) = ligne.split("\t")
#        (nomcorpus, numerophrase) = nomcorpus_numerophrase.split('_')
#        phrases.append(phrase.strip())

#for phrase in phrases:
#    result = parser.parse(phrase)
#    print(result)