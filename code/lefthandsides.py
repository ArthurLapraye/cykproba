# coding: utf8
from terminal import Terminal
from nonterminal import Nonterminal
from handside import Handside
from collections import defaultdict


class Lefthandside(Handside):
    def __init__(self, args):
        if not (((len(args) == 1) and isinstance(
                args[0], Nonterminal)) or all(isinstance(x, (Terminal, Nonterminal)) for x in args)):
            raise TypeError('Lefthandside doit être composée au minimum d\'un Nonterminal avec ou sans contexte.')
        else:
            super(Lefthandside, self).__init__(args)
            self.__lhs = args

    def __repr__(self):
        return " ".join([str(x) for x in self.__lhs])

    def __str__(self):
        return repr(self)

    def __eq__(self, other):
        if self.__lhs == other.lhs:
            return True
        else:
            return False

    def __getitem__(self, item):
        return self.__lhs[item]

    def __hash__(self):
        return 1

    def handside(self):
        return 1

    @property
    def lhs(self):
        return self.__lhs

    def replace(self, old, new):
        x = self.__handside.index(old)
        return Lefthandside(self.__handside[:x] + new + self.__handside[x+1:])


class Lefthandsidehorscontexte(Lefthandside):
    __lefthandsidehorscontexte = defaultdict(int)

    def __init__(self, args):
        if not ((len(args) == 1) and isinstance(args[0], Nonterminal)):
            raise TypeError("Une Lefthandsidehorscontexte n'est composée que d'un Nonterminal")
        else:
            super(Lefthandsidehorscontexte, self).__init__(args)
        type(self).__lefthandsidehorscontexte[str(self)] += 1

    def __getitem__(self, item):
        return type(self).__lefthandsidehorscontexte[item]

    def replace(self, old, new):
        x = self.__handside.index(old)
        return Lefthandsidehorscontexte(self.__handside[:x] + new + self.__handside[x+1:])


if __name__ == '__main__':
    x = Lefthandsidehorscontexte((Nonterminal("X"),))
    print(x["X"])
