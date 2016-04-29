# coding: utf8

from ProductionHorsContexteLexicale import ProductionHorsContexteLexicale
from Probabilite import Probabilite


class ProductionHorsContexteLexicaleProbabilisee(ProductionHorsContexteLexicale, Probabilite):
    def __init__(self, lhs, rhs, proba):
        super(ProductionHorsContexteLexicaleProbabilisee, self).__init__(lhs, rhs)
        self.proba = proba

    def __repr__(self):
        return ...

    def __str__(self):
        return repr(self)