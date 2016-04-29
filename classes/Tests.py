# coding: utf8


class Nonterminal(object):
    def __init__(self, nonterminal):
        self.nonterminal = nonterminal

class Terminal(object):
    def __init__(self, terminal):
        self.terminal = terminal

class Production(object):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

class Unaire(object):
    def __init__(self, rhs):
        assert isinstance(rhs, Nonterminal)
        self.rhs = rhs

class ProductionUnaire(Production, Unaire):
    def __init__(self, lhs, rhs):
        super(ProductionUnaire, self).__init__(lhs, rhs)
        assert isinstance(rhs, Nonterminal), "Je veux une partie droite Nonterminal"


