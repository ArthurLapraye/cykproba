# coding: utf8
from collections import defaultdict


class Terminal(object):
    __terminals = defaultdict(int)


    def __init__(self, terminal):
        self.__terminal = terminal
        type(self).__terminals[self] += 1

    @property
    def terminal(self):
        return self.__terminal

    def __repr__(self):
        return self.__terminal

    def __str__(self):
        return repr(self)

    def __len__(self):
        return 1

    def __eq__(self, other):
        if self.__dict__ == other.__dict__:
            return True
        return False

    def __hash__(self):
        return 1

    @staticmethod
    def getterminals(key=None):
        if key is not None:
            return Terminal.__terminals[key]
        else:
            return Terminal.__terminals

if __name__ == '__main__':
    x = Terminal("X")
    y = Terminal("X")
    print(Terminal.getterminals())
