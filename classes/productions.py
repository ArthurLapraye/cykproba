# coding: utf8

from collections import defaultdict
from Terminal import Terminal
from Nonterminal import Nonterminal


class Production(object):
    ___productions = set()

    def __init__(self, lhs, rhs):
        self.__lhs = lhs
        self.__rhs = rhs
        self.getproductions.add(self)


    @property
    def getlhs(self):
        return self.__lhs

    @property
    def getrhs(self):
        return self.__rhs

    @property
    def getproductions(self):
        return type(self).___productions

    @getproductions.setter
    def getproductions(self, value):
        pass

    def is_horscontexte(self):
        if isinstance(self.getlhs, Nonterminal):
            return True

    def is_binary(self):
        if (len(self.getrhs) == 2) and all(isinstance(x, Nonterminal) for x in self.getrhs):
            return True
        else:
            return False

    def is_unary(self):
        if isinstance(self.getrhs, Nonterminal):
            return True
        else:
            return False

    def is_lexical(self):
        if isinstance(self.getrhs, Terminal):
            return True
        else:
            return False

    def repre(self):
        return (str(self.getlhs), str(self.getrhs))


class ProductionHorsContexte(Production):
    def __init__(self, lhs, rhs):
        super(ProductionHorsContexte, self).__init__(lhs, rhs)
        assert isinstance(lhs, Nonterminal)

    def __repr__(self):
        return ...

    def __str__(self):
        return repr(self)


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


class ProductionHorsContexteBinaireProbabilisee(ProductionHorsContexteBinaire, Probabilite):
    def __init__(self, lhs, rhs, proba):
        ProductionHorsContexteBinaire.__init__(self, lhs, rhs)
        Probabilite.__init__(self, proba)

    def __repr__(self):
        return

    def __str__(self):
        return repr(self)


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


class ProductionHorsContexteUnaireProbabilisee(ProductionHorsContexteUnaire, Probabilite):
    def __init__(self, lhs, rhs, proba):
        super(ProductionHorsContexteUnaireProbabilisee, self).__init__(lhs, rhs)
        self.proba = proba

    def __repr__(self):
        return ...

    def __str__(self):
        return repr(self)


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


class ProductionHorsContexteLexicaleProbabilisee(ProductionHorsContexteLexicale, Probabilite):
    def __init__(self, lhs, rhs, proba):
        super(ProductionHorsContexteLexicaleProbabilisee, self).__init__(lhs, rhs)
        self.proba = proba

    def __repr__(self):
        return ...

    def __str__(self):
        return repr(self)
