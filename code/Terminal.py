# coding: utf8


class Terminal(object):

    __terminals = []

    def __init__(self, terminal):
        self.__terminal = terminal
        if self not in type(self).__terminals:
            Terminal.__terminals.append(terminal)

    @staticmethod
    def terminals():
        return Terminal.__terminals

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
        if self.__terminal == str(other):
            return True
        else:
            return False

    def __iter__(self):
        yield self


if __name__ == '__main__':
    x = Terminal("X")
    print(type(x).__name__)
    print(x.terminal)
    print(len(x))
    print(iter(x))
    print(Terminal.terminals())
