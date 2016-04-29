# coding: utf8

from ProductionHorsContexte import ProductionHorsContexte
from Nonterminal import Nonterminal


class ProductionHorsContexteBinaire(ProductionHorsContexte):
    __productionsBinaires = set([])

    def __init__(self, lhs, rhs):
        super(ProductionHorsContexteBinaire, self).__init__(lhs, rhs)
        assert (len(rhs) == 2) and (all(isinstance(x, Nonterminal) for x in rhs))
        self.getproductionsBinaires.add(self)

    @property
    def getproductionsBinaires(self):
        return type(self).__productionsBinaires

    @getproductionsBinaires.setter
    def getproductionsBinaires(self, value):
        pass

    def __repr__(self):
        return ...

    def __str__(self):
        return repr(self)
