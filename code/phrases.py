# coding: utf8

class Phrase(object):
    def __init__(self, gold, corpus, numero):
        self.__gold = gold
        self.__predit = ""
        self.__productions = {}
        self.__corpus = corpus
        self.__numero = numero
        self.__extraction = []

    @property
    def productions(self):
        return self.__productions

    @productions.setter
    def productions(self, value):
        pass

    @property
    def predit(self):
        return self.__predit

    @predit.setter
    def predit(self, value):
        pass

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
    def extraction(self):
        return self.__extraction

    @extraction.setter
    def extraction(self, value):
        pass

    def __repr__(self):
        return self.__gold

    def __str__(self):
        return repr(self)

if __name__ == '__main__':
    x = Phrase('bonjour', 'au revoir', 4)
