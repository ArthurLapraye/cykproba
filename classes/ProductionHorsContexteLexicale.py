# coding: utf8

from ProductionHorsContexte import ProductionHorsContexte
from Terminal import Terminal


class ProductionHorsContexteLexicale(ProductionHorsContexte):
    __productionsLexicales = set([])

    def __init__(self, lhs, rhs):
        super(ProductionHorsContexteLexicale, self).__init__(lhs, rhs)
        assert isinstance(rhs, Terminal)
        self.getproductionsLexicales.add(self)

    @property
    def getproductionsLexicales(self):
        return type(self).__productionsLexicales

    @getproductionsLexicales.setter
    def getproductionsLexicales(self, value):
        pass

    def __repr__(self):
        return ...

    def __str__(self):
        return repr(self)