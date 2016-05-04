# coding: utf8

from collections import defaultdict
from terminal import Terminal
from nonterminal import Nonterminal
from probabilite import Probabilite
from lefthandsides import *
from righthandsides import *


class Production():
    ___productions = set()

    def __init__(self, lhs, rhs):
        self.lhs = Lefthandside(lhs)
        self.rhs = Righthandside(rhs)

        self.getproductions.add(self)

    @property
    def getproductions(self):
        return type(self).___productions

    @getproductions.setter
    def getproductions(self, value):
        pass

    def is_horscontexte(self):
        if isinstance(self.lhs, LefthandsideHorsContexte):
            return True

    def is_binary(self):
        if isinstance(self.rhs, RighthandsideBinaire):
            return True
        else:
            return False

    def is_unary(self):
        if isinstance(self.rhs, RighthandsideUnaire):
            return True
        else:
            return False

    def is_lexical(self):
        if isinstance(self.rhs, RighthandsideLexicale):
            return True
        else:
            return False

    def __repr__(self):
        return "({0} {1})".format(self.lhs, self.rhs)

    def __str__(self):
        return repr(self)


class ProductionHorsContexte(Production):
    def __init__(self, lhs, rhs):
        super(ProductionHorsContexte, self).__init__(lhs, rhs)
        self.lhs = LefthandsideHorsContexte(lhs)


class ProductionHorsContexteBinaire(ProductionHorsContexte):
    __productionsBinaires = set([])

    def __init__(self, lhs, rhs):
        super(ProductionHorsContexteBinaire, self).__init__(lhs, rhs)
        self.rhs = RighthandsideBinaire(rhs)

        self.getproductionsBinaires.add(self)

    @property
    def getproductionsBinaires(self):
        return type(self).__productionsBinaires


class ProductionHorsContexteBinaireProbabilisee(ProductionHorsContexteBinaire):
    def __init__(self, lhs, rhs, proba):
        ProductionHorsContexteBinaire.__init__(self, lhs, rhs)
        self.__proba = Probabilite(
            numerator=proba[0],
            denominator=proba[1]
        )

    @property
    def proba(self):
        return self.__proba

    def __repr__(self):
        return " ".join([super(ProductionHorsContexteBinaireProbabilisee, self).__repr__(), str(self.__proba)])

    def __str__(self):
        return repr(self)


class ProductionHorsContexteUnaire(ProductionHorsContexte):
    __productionsUnaires = set([])

    def __init__(self, lhs, rhs):
        super(ProductionHorsContexteUnaire, self).__init__(lhs, rhs)
        self.rhs = RighthandsideUnaire(rhs)

        self.getproductionsUnaires.add(self)

    @property
    def getproductionsUnaires(self):
        return type(self).__productionsUnaires

    @getproductionsUnaires.setter
    def getproductionsUnaires(self, value):
        pass


class ProductionHorsContexteUnaireProbabilisee(ProductionHorsContexteUnaire):
    def __init__(self, lhs, rhs, proba):
        super(ProductionHorsContexteUnaireProbabilisee, self).__init__(lhs, rhs)
        self.__proba = Probabilite(
            numerator=proba[0],
            denominator=proba[1]
        )

    @property
    def proba(self):
        return self.__proba

    def __repr__(self):
        return " ".join([super(ProductionHorsContexteUnaireProbabilisee, self).__repr__(), str(self.__proba)])

    def __str__(self):
        return repr(self)


class ProductionHorsContexteLexicale(ProductionHorsContexte):
    __productionsLexicales = set([])

    def __init__(self, lhs, rhs):
        super(ProductionHorsContexteLexicale, self).__init__(lhs, rhs)
        self.rhs = RighthandsideLexicale(rhs)

        self.getproductionsLexicales.add(self)

    @property
    def getproductionsLexicales(self):
        return type(self).__productionsLexicales

    @getproductionsLexicales.setter
    def getproductionsLexicales(self, value):
        pass


class ProductionHorsContexteLexicaleProbabilisee(ProductionHorsContexteLexicale):
    def __init__(self, lhs, rhs, proba):
        super(ProductionHorsContexteLexicaleProbabilisee, self).__init__(lhs, rhs)
        self.__proba = Probabilite(
            numerator=proba[0],
            denominator=proba[1]
        )

    @property
    def proba(self):
        return self.__proba

    def __repr__(self):
        return " ".join([super(ProductionHorsContexteLexicaleProbabilisee, self).__repr__(), str(self.__proba)])

    def __str__(self):
        return repr(self)
