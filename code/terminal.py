# coding: utf8
import collections


def terminal_representer(dumper, data):
    return dumper.represent_scalar("!terminal", str(data))


class Terminal(collections.Sequence):
    __terminals = set()
    def __init__(self, string):
        self.__list = string
        self.__terminals.add(self)

    @property
    def list(self):
        return self.__list

    def check_type(self):
        if not isinstance(self.__chaine, str):
            raise TypeError('Une {name} doit être une string'.format(name=self.__class__.__name__))

    def __eq__(self, other):
        if self.__dict__ == other.__dict__:
            return True
        return False

    def __hash__(self): return 0

    def __len__(self): return len(self.__list)

    def __getitem__(self, i): return self.__list[i]

    def __repr__(self): return str(self.__list)

    def __str__(self): return repr(self)

    @staticmethod
    def terminals():
        return Terminal.__terminals


if __name__ == '__main__':
    pass
