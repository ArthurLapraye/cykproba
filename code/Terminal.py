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

    def __iter__(self):
        yield self


if __name__ == '__main__':
    x = Terminal("X")
    print(type(x).__name__)
    print(x.terminal)
    print(len(x))
    print(iter(x))
    print(x.terminals)
