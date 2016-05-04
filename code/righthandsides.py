# coding: utf8

from nonterminal import Nonterminal
from terminal import Terminal


class Righthandside(object):
    def __init__(self, rhs):
        if all(isinstance(x, (Terminal, Nonterminal)) for x in rhs):
            self.__rhs = rhs
        else:
            raise TypeError("Une Righthandside est composée de Terminal et/ou de Nonterminal.")

    @property
    def __getrhs(self):
        return self.__rhs

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
        # Righthandside.__init__(self, rhs)
        if isinstance(rhs, Terminal):
            self._Righthandside__rhs = rhs
        else:
            raise TypeError("Une RighthandsideLexicale est composée d'un Terminal.")

    # def __repr__(self):
    #     return self.getrhs

    # def __str__(self):
    #     return repr(self)


class RighthandsideUnaire(Righthandside):
    """

    """
    def __init__(self, rhs):
        # super(RighthandsideUnaire, self).__init__(rhs)
        if isinstance(rhs, Nonterminal):
            self._Righthandside__rhs = rhs
        else:
            raise TypeError("Une RighthandsideUnaire est composée d'un Nonterminal.")

    # def __repr__(self):
    #     return "({0})".format(" ".join([str(x) for x in self.getrhs]))

    # def __str__(self):
    #     return repr(self)


class RighthandsideBinaire(Righthandside):
    """

    """
    def __init__(self, rhs):
        # super(RighthandsideBinaire, self).__init__(rhs)
        if (len(rhs) == 2) and all(isinstance(x, Nonterminal) for x in rhs):
            self._Righthandside__rhs = rhs
        else:
            raise TypeError("Une RighthandsideBinaire est composée de deux Nonterminal.")

    # def __repr__(self):
    #     return "({0})".format(" ".join([str(x) for x in self.getrhs]))

    # def __str__(self):
    #     return repr(self)

# x = RighthandsideBinaire([Nonterminal('E'), Nonterminal('Z')])
# print(x)