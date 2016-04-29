# coding: utf8

from ProductionHorsContexte import ProductionHorsContexte
from Nonterminal import Nonterminal
from Terminal import Terminal

class ProductionHorsContexteUnaire(ProductionHorsContexte):
    __productionsUnaires = set([])

    def __init__(self, lhs, rhs):
        super(ProductionHorsContexteUnaire, self).__init__(lhs, rhs)
        assert isinstance(rhs, Nonterminal)
        self.getproductionsUnaires.add(self)

    @property
    def getproductionsUnaires(self):
        return type(self).__productionsUnaires

    @getproductionsUnaires.setter
    def getproductionsUnaires(self, value):
        pass

    def __repr__(self):
        return ...

    def __str__(self):
        return repr(self)