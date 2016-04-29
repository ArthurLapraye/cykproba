# coding: utf8

from ProductionHorsContexteBinaire import ProductionHorsContexteBinaire
from Probabilite import Probabilite


class ProductionHorsContexteBinaireProbabilisee(ProductionHorsContexteBinaire, Probabilite):
    def __init__(self, lhs, rhs, proba):
        ProductionHorsContexteBinaire.__init__(self, lhs, rhs)
        Probabilite.__init__(self, proba)

    def __repr__(self):
        return

    def __str__(self):
        return repr(self)
