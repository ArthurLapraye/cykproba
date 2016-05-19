# coding: utf8
from terminal import Terminal
from nonterminal import Nonterminal

class Handside(object):
    def __init__(self, args):
        if not all(isinstance(x, (Terminal, Nonterminal)) for x in args):
            raise TypeError('Handside ne doit être composée que de Terminal ou de Nonterminal')
        else:
            self.__handside = args

    def __repr__(self):
        return " ".join([str(x) for x in self.__handside])

    def __str__(self):
        return repr(self)

    def __len__(self):
        return len(self.__handside)

    @property
    def handside(self):
        return self.__handside

    @property
    def handside(self, value):
        return self.__handside

    def replace(self, old, new):
        x = self.__handside.index(old)
        return Handside(self.__handside[:x] + new + self.__handside[x+1:])

if __name__ == '__main__':
    x = Handside((Nonterminal("X"), Nonterminal("Y"), Terminal("ont")))
    y = Handside((Nonterminal('Y'), Nonterminal("Z")))
#    print(type(x|y))
