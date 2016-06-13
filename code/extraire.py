# coding: utf-8
import ply.lex as lex
import ply.yacc as yacc
import nonterminal
import terminal
import productions
import lefthandside
import righthandside


sentence = []

#################### PARTIE LEXICALE #####################################

literals = '()'

tokens = ('MOT',)

# Cette expression régulière tente de carpter tout caractère ne faisant pas partie
def t_MOT(t):
    r"""[\µ\©\#\±\°\á\Î\É\ÀA-Za-z0-9\ó\-\_\+\à\â\ä\é\è\ê\ë\î\ï\ô\ö\ù\ü\û\ç\'\.\,\:\;\/\"\ß\?\%\<\>\=\[\]\&\!\^\$\½][\©\µ\#\½\±\°\ó\á\Î\$\!\^\&\É\ÀA-Za-z0-9\-\_\+\'\.\,\à\â\ä\é\è\ê\ë\î\ï\ô\ö\ù\ü\û\ç\:\;\/\"ß\?\%\<\>\=\[\]]*"""
    return t


def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += len(t.value)


t_ignore = ' '


def t_error(t):
    print("Illegal character {0}".format(t.value[0]))
    t.lexer.skip(1)

lex.lex(
    optimize=1,
    lextab="lexique"
)

#################### PARTIE SYNTAXIQUE ####################################

# Règle permettant de rendre la grammaire non ambigue.
#
def p_axiome(p):
    """Sprim : '(' S ')'"""
    # p[0] = p[2][0]
    p[0] = sentence


# Cette grammaire comprte deux S, soit une règle lexicale, soit un syntagme complexe.
# p_s_1 représente le syntagme complexe.
def p_s_1(p):
    """S : '(' syntagme ')'"""
    p[0] = p[2]


# p_s_2 représente le syntagme lexical.
def p_s_2(p):
    """ S : '(' lexique ')' """
    p[0] = p[2]


# Règle permttant de capter les productions unaires, binaires et naires.
def p_syntagme(p):
    """ syntagme : head exprs """
    rhs = [x[0] for x in p[2]]

    if len(rhs) == 1:
        productions.Productionhorscontexte1unaireprobabilisee(
            lefthandside.Lefthandsidehorscontexte(p[1]),
            righthandside.Righthandside1unaire(*rhs)
        )
    elif len(p[2]) == 2:
        productions.Productionhorscontexte2binaireprobabilisee(
            lefthandside.Lefthandsidehorscontexte(p[1]),
            righthandside.Righthandside2binaire(*rhs)
        )
    else:
        productions.ProductionhorscontexteNaireprobabilisee(
            lefthandside.Lefthandsidehorscontexte(p[1]),
            righthandside.RighthandsideNaire(*rhs)
        )

    p[0] = [[p[1], p[2]]]


# p_exprs tente de regrouper ensembles les membres de la partie droite d'une règle.
# donc si une règle fait : X > A Z E R. Elle va faire en sorte que A, Z, E, et R soit une liste.
def p_exprs(p):
    """ exprs : S exprs
              | S
    """

    if len(p) == 3:
        p[1].extend(p[2])
        p[0] = p[1]
    else:
        p[0] = p[1]


# Cette règle représente une production lexicale
# Les parties commentées sont les différentes possibilités que l'on peut faire
# soit extraire une grammaire avec le lexique soit avec les mots de la langue
# soit avec ou sans les fonctions syntaxiques.
# soit en remplaçant les mots du lexique par leur étiquette morphosyntaxique.
def p_lexique(p):
    """ lexique : head leaf """

    # Première version avec le lexique et les fonctions syntaxiques

    # productions.Productionhorscontexte1lexicaleprobabilisee([p[1]], [p[2]])

    # Deuxième version avec le lexique sans les fonctions syntaxiques

    leaf = terminal.Terminal(p[1].list.lower())
    sentence.append(leaf)
    productions.Productionhorscontexte1lexicaleprobabilisee(
        lefthandside.Lefthandsidehorscontexte(p[1]),
        righthandside.Righthandside1lexicale(leaf)
    )

    # Dernière version sans le lexique ni les fonctions syntaxiques
<<<<<<< HEAD

#    temp = p[1][0].split('-')[0]
#    head = nonterminal.Nonterminal(temp)
#    leaf = terminal.Terminal(temp.lower())
    p[0] = [[p[1], leaf]]
=======
    
    temp = p[1].nonterminal.split('-')[0]
    head = nonterminal.Nonterminal(temp)
    leaf = terminal.Terminal

    p[0] = [[p[1], p[2]]]
>>>>>>> origin/master


def p_head(p):
    """ head : MOT """
    p[0] = nonterminal.Nonterminal(p[1].split('-')[0])


def p_leaf(p):
    """ leaf : MOT """
    p[0] = terminal.Terminal(p[1])


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

########################################################################

if __name__ == '__main__':
    pass
