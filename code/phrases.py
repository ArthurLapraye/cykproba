# coding: utf8


class Phrase(object):
    """

    """
    __phrases = []

    def __init__(self, phrase):
        self.phrase = phrase
        self.pos = self.phrase2pos()
        self.binary = self.phrase2binary()

    @property
    def get_binary(self):
        return self.binary

    @property
    def get_phrases(self):
        return type(self).__phrases

    def phrase2binary(self):
        pass

    def phrase2pos(self):
        pass

    def unbinarise(self):
        pass



