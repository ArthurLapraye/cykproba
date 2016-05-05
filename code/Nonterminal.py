# coding: utf8

class Nonterminal(object):

    __nonterminals = set([])

    def __init__(self, nonterminal):
        self.__nonterminal = nonterminal
        type(self).__nonterminals.add(self)

    @property
    def nonterminal(self):
        return self.__nonterminal

    @staticmethod
    def nonterminals():
        return Nonterminal.__nonterminals

    def __repr__(self):
        return self.__nonterminal

    def __str__(self):
        return repr(self)

    def __len__(self):
        return 1

    def __iter__(self):
        yield self

if __name__ == '__main__':
    x = Nonterminal("X")
    print(type(x).__name__)
    print(x.nonterminal)
    print(len(x))
    print(iter(x))