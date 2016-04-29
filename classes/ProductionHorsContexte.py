# coding: utf8

from Production import Production
from Nonterminal import Nonterminal
from Terminal import Terminal


class ProductionHorsContexte(Production):
    def __init__(self, lhs, rhs):
        super(ProductionHorsContexte, self).__init__(lhs, rhs)
        assert isinstance(lhs, Nonterminal)

    def __repr__(self):
        return ...

    def __str__(self):
        return repr(self)