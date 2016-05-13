# coding: utf8

from collections import defaultdict
from terminal import Terminal
from nonterminal import Nonterminal
from probabilite import Probabilite
from lefthandsides import *
from righthandsides import *


class Production():
    ___productions = set([])

    def __init__(self, lhs, rhs):
        self.lhs = Lefthandside(lhs)
        self.rhs = Righthandside(rhs)

        self.___productions.add(self)

    @staticmethod
    def getproductions():
        return Production.___productions

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

    @staticmethod
    def vider_productions():
        Production.___productions = set([])

    def __repr__(self):
        return "({0} {1})".format(self.lhs, self.rhs)

    def __str__(self):
        return repr(self)


class ProductionHorsContexte(Production):
    def __init__(self, lhs, rhs):
        super(ProductionHorsContexte, self).__init__(lhs, rhs)
        self.lhs = LefthandsideHorsContexte(lhs)

    @staticmethod
    def ununarise():
        productions = Production.getproductions()
        for gunary in [x for x in productions if isinstance(x, ProductionHorsContexteUnaire)]:
            new_nt = Nonterminal("|".join([str(gunary.lhs), str(gunary.rhs)]))
            for dunary in [x for x in productions if gunary.lhs in x.rhs]:
                new_droite = dunary.rhs.replace(gunary.lhs, new_nt)
                ProductionHorsContexte(dunary.lhs, new_droite)
            for funary in [x for x in productions if gunary.rhs == x.lhs]:
                ProductionHorsContexte(new_nt, funary.rhs)

    def getprodunaire(self):
        return [x for x in type(self).___productions if isinstance(x, ProductionHorsContexteUnaire)]

    def getprodbinaire(self):
        return [x for x in type(self).___productions if isinstance(x, ProductionHorsContexteBinaire)]

    def getprodlexicale(self):
        return [x for x in type(self).___productions if isinstance(x, ProductionHorsContexteLexicale)]

    def getproductionnaire(self):
        return [x for x in type(self).___productions if isinstance(x, ProductionHorsContexte)]


class ProductionHorsContexteProbabilisee(ProductionHorsContexte):
    def __init__(self, lhs, rhs, proba):
        super(ProductionHorsContexteProbabilisee, self).__init__(lhs, rhs)
        self.__proba = Probabilite(
            numerator=proba[0],
            denominator=proba[1]
        )

    @property
    def proba(self):
        return self.__proba

    @staticmethod
    def ununarise():
        productions = Production.getproductions()
        for gunary in ProductionHorsContexteProbabilisee.getprodunaire():
            new_nt = Nonterminal("|".join([str(gunary.lhs), str(gunary.rhs)]))
            for dunary in [x for x in productions if gunary.lhs in x.rhs]:
                new_droite = dunary.rhs.replace(gunary.lhs, new_nt)
                ProductionHorsContexteProbabilisee(dunary.lhs, new_droite)
            for funary in [x for x in productions if gunary.rhs == x.lhs]:
                ProductionHorsContexteProbabilisee(new_nt, funary.rhs)

    @staticmethod
    def binarise():
        for nary in ProductionHorsContexteProbabilisee.getprodnaire():
            pass

    @staticmethod
    def getprodunaire():
        return [x for x in ProductionHorsContexteProbabilisee.___productions if isinstance(x, ProductionHorsContexteUnaireProbabilisee)]

    @staticmethod
    def getprodbinaire():
        return [x for x in ProductionHorsContexteProbabilisee.___productions if isinstance(x, ProductionHorsContexteBinaireProbabilisee)]

    @staticmethod
    def getprodlexicale():
        return [x for x in ProductionHorsContexteProbabilisee.___productions if isinstance(x, ProductionHorsContexteLexicaleProbabilisee)]

    @staticmethod
    def getprodnaire():
        return [x for x in ProductionHorsContexteProbabilisee.___productions if isinstance(x, ProductionHorsContexteProbabilisee)]

    def __repr__(self):
        return " ".join([super(ProductionHorsContexteProbabilisee, self).__repr__(), str(self.__proba)])

    def __str__(self):
        return repr(self)


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

if __name__ == '__main__':
    x = Production(Nonterminal("X"), [Nonterminal('X'), Terminal('r')])
    print(x)
    y = ProductionHorsContexte(Nonterminal("X"), [Nonterminal("Y"), Terminal('r')])
    print(y)
    a = ProductionHorsContexteBinaire(Nonterminal("X"), [Nonterminal("Y"), Nonterminal("Z")])
    print(a)
    b = ProductionHorsContexteBinaireProbabilisee(Nonterminal("X"), [Nonterminal("Y"), Nonterminal("Z")], (1, 4))
    print(b)
    c = ProductionHorsContexteLexicale(Nonterminal("X"), Terminal("x"))
    print(c)
    d = ProductionHorsContexteLexicaleProbabilisee(Nonterminal("X"), Terminal("x"), (12, 90))
    print(d)
    e = ProductionHorsContexteUnaire(Nonterminal("X"), Nonterminal("X"))
    print(e)
    f = ProductionHorsContexteUnaireProbabilisee(Nonterminal("X"), Nonterminal("x"), (52, 50))
    print(f)
