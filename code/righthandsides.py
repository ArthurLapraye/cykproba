# coding: utf8

from Nonterminal import Nonterminal
from Terminal import Terminal


class Righthandside(object):
    def __init__(self, rhs):
        self.rhs = rhs


class RighthandsideLexicale(Righthandside):
    pass


class RighthandsideUnaire(Righthandside):
    pass


class RighthandsideBinaire(Righthandside):
    pass
