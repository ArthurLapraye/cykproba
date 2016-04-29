# coding: utf8

from ProductionHorsContexteNaire import ProductionHorsContexteNaire
from Probabilite import Probabilite


class ProductionHorsContexteNaireProbabilisee(ProductionHorsContexteNaire, Probabilite):
    def __init__(self, lhs, rhs, proba):
        super(ProductionHorsContexteNaireProbabilisee, self).__init__(lhs, rhs)
        self.proba = proba

    def __repr__(self):
        return ...

    def __str__(self):
        return repr(self)