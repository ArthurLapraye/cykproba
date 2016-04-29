# coding: utf8

from ProductionHorsContexteUnaire import ProductionHorsContexteUnaire
from Probabilite import Probabilite


class ProductionHorsContexteUnaireProbabilisee(ProductionHorsContexteUnaire, Probabilite):
    def __init__(self, lhs, rhs, proba):
        super(ProductionHorsContexteUnaireProbabilisee, self).__init__(lhs, rhs)
        self.proba = proba

    def __repr__(self):
        return ...

    def __str__(self):
        return repr(self)