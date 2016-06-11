# coding: utf8


class Phrase(object):
    __phrases = []
    def __init__(self, gold, pos, corpus=None, numero=None):
        self.__gold = gold
        self.__corpus = corpus
        self.__numero = numero
        self.__pos_gold = pos
        self.__predit = ""

        if self not in self.__phrases:
            self.__phrases.append(self)

    @property
    def predit(self):
        return self.__predit

    @predit.setter
    def predit(self, value):
        self.__predit = value

    @property
    def gold(self):
        return self.__gold

    @property
    def corpus(self):
        return self.__corpus

    @property
    def numero(self):
        return self.__numero

    @property
    def pos_gold(self):
        return self.__pos_gold

    def unbinarise(self):
        pass

    @staticmethod
    def phrases():
        return Phrase.__phrases

    def __eq__(self, other):
        if self.gold == other.gold:
            return True
        return False

    def __hash__(self):
        return 1

    def __repr__(self):
        return self.__gold

    def __str__(self):
        return repr(self)


if __name__ == '__main__':
    pass
