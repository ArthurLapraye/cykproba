# coding: utf8


class Phrase(object):
    """

    """
    __phrases = []

    def __init__(self, phrase):
        self.phrase = phrase

    @property
    def get_phrases(self):
        return type(self).__phrases
