# coding: utf8

from ProductionHorsContexte import ProductionHorsContexte
from Nonterminal import Nonterminal
from Terminal import Terminal


class ProductionHorsContexteNaire(ProductionHorsContexte):
    __productionsNaires = set([])

    def __init__(self, lhs, rhs):
        super(ProductionHorsContexteNaire, self).__init__(lhs, rhs)
        if len(rhs) > 1:
            assert all(isinstance(x, (Nonterminal, Terminal)) for x in rhs), ""
        else:
            assert isinstance(rhs, (Nonterminal, Terminal)), ""
        self.getproductionsNaires.add(self)

    @property
    def getproductionsNaires(self):
        return type(self).__productionsNaires

    @getproductionsNaires.setter
    def getproductionsNaires(self, value):
        pass

    def __repr__(self):
        return ...

    def __str__(self):
        return repr(self)