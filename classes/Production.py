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
