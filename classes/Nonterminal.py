# coding: utf8

class Nonterminal(object):

    _nonterminals = set([])

    def __init__(self, nonterminal):
        self.__nonterminal = nonterminal
        self.nonterminals.add(nonterminal)

    @property
    def nonterminal(self):
        return self.__nonterminal

    @property
    def nonterminals(self):
        return type(self)._nonterminals

    @nonterminals.setter
    def nonterminals(self, value):
        pass

    def __repr__(self):
        return self.nonterminal

    def __str__(self):
        return repr(self)

    def __len__(self):
        return 1