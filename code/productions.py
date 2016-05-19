# coding: utf8

from lefthandside import *
from righthandside import *
from nonterminal import Nonterminal
from terminal import Terminal
from fractions import Fraction
from collections import defaultdict


class Production(object):
    __productions = []

    def __init__(self, lhs, rhs):
        self.__lhs = Lefthandside(lhs)
        self.__rhs = Righthandside(rhs)

        if self not in type(self).__productions:
            type(self).__productions.append(self)

    def __repr__(self):
        return str(self.__lhs) + " > " + str(self.__rhs)

    def __str__(self):
        return repr(self)

    def __eq__(self, other):
        if (self.__lhs == other.lhs) and (self.__rhs == other.rhs):
            return True
        else:
            return False

    def __hash__(self):
        return 1

    @property
    def rhs(self):
        return self.__rhs

    @property
    def lhs(self):
        return self.__lhs

    @lhs.setter
    def lhs(self, value):
        pass

    @staticmethod
    def productions():
        return Production.__productions

    @staticmethod
    def getproductions(productions, cls):
        return [x for x in productions if issubclass(type(x), cls)]


class Productionhorscontexte(Production):
    def __init__(self, lhs, rhs):
        # super(Productionhorscontexte, self).__init__(lhs, rhs)
        Production.__init__(self, lhs, rhs)
        self.__lhs = Lefthandsidehorscontexte(lhs)
        self.__rhs = Righthandside(rhs)

    @property
    def lhs(self):
        return self.__lhs

    @lhs.setter
    def lhs(self, value):
        pass

    @property
    def getrhs(self):
        return self.__rhs


class Productionhorscontextebinaire(Productionhorscontexte):
    def __init__(self, lhs, rhs):
        Productionhorscontexte.__init__(self, lhs, rhs)
        # super(Productionhorscontextebinaire, self).__init__(lhs, rhs)
        self.__rhs = Righthandside2binaire(rhs)


class Productionhorscontextenaire(Productionhorscontexte):
    def __init__(self, lhs, rhs):
        super(Productionhorscontextenaire, self).__init__(lhs, rhs)
        self.__rhs = RighthandsideNaire(rhs)


class Productionhorscontexteempty(Productionhorscontexte):
    def __init__(self, lhs, rhs):
        super(Productionhorscontexteempty, self).__init__(lhs, rhs)
        self.__rhs = Righthandside0(rhs)


class Productionhorscontextelexicale(Productionhorscontexte):
    def __init__(self, lhs, rhs):
        super(Productionhorscontextelexicale, self).__init__(lhs, rhs)
        self.__rhs = Righthandside1lexicale(rhs)


class Productionhorscontexteunaire(Productionhorscontexte):
    def __init__(self, lhs, rhs):
        super(Productionhorscontexteunaire, self).__init__(lhs, rhs)
        self.__rhs = Righthandside1unaire(rhs)

    @property
    def getrhs(self):
        return self.__rhs


class Productionhorscontexteprobabilisee(Productionhorscontexte):
    __productionshorscontexteprobabilisees = defaultdict(int)

    def __init__(self, lhs, rhs):
        super(Productionhorscontexteprobabilisee, self).__init__(lhs, rhs)

        self.__proba = Fraction(1, 1)

        type(self).__productionshorscontexteprobabilisees[str(self)] += 1

    @staticmethod
    def setprobaproductions():
        for p in Production.getproductions(Production.productions(), Productionhorscontexteprobabilisee):
            p.setproba()

    @property
    def proba(self):
        return self.__proba

    @proba.setter
    def proba(self, value):
        pass

    def setproba(self):
        self.__proba = Fraction(self[str(self)], self.lhs[str(self.lhs)])

    def __repr__(self):
        return "{self.lhs} > {self.rhs} : {self.proba}".format(self=self)

    def __str__(self):
        return repr(self)

    def __getitem__(self, item):
        return type(self).__productionshorscontexteprobabilisees[item]


class Productionhorscontexteprobabiliseebinaire(Productionhorscontexteprobabilisee):
    def __init__(self, lhs, rhs):
        super(Productionhorscontexteprobabiliseebinaire, self).__init__(lhs, rhs)
        self.__rhs = Righthandside2binaire(rhs)


class Productionhorscontexteprobabiliseenaire(Productionhorscontexteprobabilisee):
    def __init__(self, lhs, rhs):
        super(Productionhorscontexteprobabiliseenaire, self).__init__(lhs, rhs)
        self.__rhs = RighthandsideNaire(rhs)


class Productionhorscontexteprobabiliseeempty(Productionhorscontexteprobabilisee):
    def __init__(self, lhs, rhs):
        super(Productionhorscontexteprobabiliseeempty, self).__init__(lhs, rhs)
        self.__rhs = Righthandside0(rhs)


class Productionhorscontexteprobabilisee1(Productionhorscontexteprobabilisee):
    def __init__(self, lhs, rhs):
        super(Productionhorscontexteprobabilisee1, self).__init__(lhs, rhs)
        self.__rhs = Righthandside1(rhs)


class Productionhorscontexteprobabiliseelexicale(Productionhorscontexteprobabilisee1):
    def __init__(self, lhs, rhs):
        super(Productionhorscontexteprobabiliseelexicale, self).__init__(lhs, rhs)
        self.__rhs = Righthandside1lexicale(rhs)


class Productionhorscontexteprobabiliseeunaire(Productionhorscontexteprobabilisee1):
    def __init__(self, lhs, rhs):
        super(Productionhorscontexteprobabiliseeunaire, self).__init__(lhs, rhs)
        self.__rhs = Righthandside1unaire(rhs)

if __name__ == '__main__':
    pass
    # lhs = (Nonterminal("X"),Nonterminal('R'))
    # rhs = ((Nonterminal("X"),), (Nonterminal("X"),Nonterminal("Y")), (Terminal('r'),), (Nonterminal("X"), Nonterminal('R'), Terminal('ons'), Nonterminal("Z")))

    a = Productionhorscontextebinaire((Nonterminal("X"),), (Nonterminal("R"), Nonterminal('ons')))
    z = Productionhorscontexteprobabilisee((Nonterminal("X"),), (Nonterminal("R"), Terminal('ons')))
    e = Productionhorscontexteprobabilisee((Nonterminal("X"),), (Nonterminal('T'), ))
    f = Productionhorscontexte((Nonterminal("X"),), (Nonterminal('T'), ))
    print(f.lhs)