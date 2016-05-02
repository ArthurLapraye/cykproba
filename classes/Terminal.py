# coding: utf8

class Terminal(object):

    __terminals = set([])

    def __init__(self, terminal):
        self.__terminal = terminal
        type(self).__terminals.add(terminal)

    @property
    def terminals(self):
        return type(self).__terminals

    @property
    def terminal(self):
        return self.__terminal

    def __repr__(self):
        return self.__terminal

    def __str__(self):
        return repr(self)

    def __len__(self):
        return 1
