# coding: utf8

from nonterminal import Nonterminal
from terminal import Terminal


class Righthandside(object):
    def __init__(self, rhs):
        if all(isinstance(x, (Terminal, Nonterminal)) for x in rhs):
            self.__rhs = rhs
        else:
            raise TypeError("Une Righthandside est composée de Terminal et/ou de Nonterminal.")

    def __repr__(self):
        if len(self.__rhs) != 1:
            return "({0})".format(" ".join([str(x) for x in self.__rhs]))
        else:
            return "{0}".format(" ".join([str(x) for x in self.__rhs]))

    def __str__(self):
        return repr(self)


class RighthandsideLexicale(Righthandside):
    """

    """
    def __init__(self, rhs):
        if isinstance(rhs, Terminal):
            self._Righthandside__rhs = rhs
        else:
            raise TypeError("Une RighthandsideLexicale est composée d'un Terminal.")


class RighthandsideUnaire(Righthandside):
    """

    """
    def __init__(self, rhs):
        if isinstance(rhs, Nonterminal):
            self._Righthandside__rhs = rhs
        else:
            raise TypeError("Une RighthandsideUnaire est composée d'un Nonterminal.")


class RighthandsideBinaire(Righthandside):
    """

    """
    def __init__(self, rhs):
        if (len(rhs) == 2) and all(isinstance(x, Nonterminal) for x in rhs):
            self._Righthandside__rhs = rhs
        else:
            raise TypeError("Une RighthandsideBinaire est composée de deux Nonterminal.")


if __name__ == '__main__':
    x = Righthandside([Nonterminal("X"), Terminal('y')])
    print(x)
    y = RighthandsideBinaire([Nonterminal("X"), Nonterminal("R")])
    print(y)
    z = RighthandsideUnaire(Nonterminal('R'))
    print(z)
    t = RighthandsideLexicale(Terminal('r'))
    print(t)
