# coding: utf8

from Nonterminal import Nonterminal
from Terminal import Terminal


class Grammaire(object):
    def __init__(self, terminals, nonterminals, axiome, productions):
        assert isinstance(terminals, set) and all(isinstance(x, Terminal) for x in terminals), "L'alphabet terminal ne doit être composé que de terminaux"
        assert isinstance(nonterminals, set) and all(isinstance(x, Nonterminal) for x in nonterminals), "l'alphabet nonterminal ne doit être composé que de nonterminaux"
        assert isinstance(axiome, Nonterminal) and (axiome in nonterminals), "L'axiome doit nécessairement faire partie de l'ensemble nonterminals"
        assert isinstance(productions, set), "Les productions doivent être encapsulées dans un set"
        self.terminals = terminals
        self.nonterminals = nonterminals
        self.axiome = axiome
        self.productions = productions

    def __repr__(self):
        return

    def __str__(self):
        return repr(self)