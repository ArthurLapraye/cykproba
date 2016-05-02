# coding: utf8

class Probabilite(object):
    def __init__(self, proba):
        self.__proba = proba

    @property
    def proba(self):
        return self.__proba

    @proba.setter
    def proba(self, value):
        pass

    def __repr__(self):
        return ...

    def __str__(self):
        return repr(self)