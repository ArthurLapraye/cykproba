# coding: utf8

import collections


def nonterminal_representer(dumper, data):
    return dumper.represent_scalar("!nonterminal", str(data))


class Nonterminal(collections.Sequence):
    __nonterminals = set()

    def __init__(self, string):
        self.__list = string

        if self.__nonterminals != set():
            if not any(self.__list == x.list for x in self.__nonterminals):
                self.__nonterminals.add(self)
        else:
            self.__nonterminals.add(self)

    @property
    def list(self):
        return self.__list

    def check_type(self):
        if not isinstance(self.__list, str):
            raise TypeError('Une {name} doit être une string'.format(name=self.__class__.__name__))

    def __len__(self): return len(self.__list)

    def __getitem__(self, i): return self.__list[i]

    def __repr__(self): return str(self.__list)

    def __str__(self): return repr(self)

    def __eq__(self, other):
        if self.__dict__ == other.__dict__:
            return True
        return False

    def __hash__(self): return 0

    @staticmethod
    def nonterminals():
        return Nonterminal.__nonterminals

if __name__ == '__main__':
    pass
