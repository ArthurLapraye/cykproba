# coding: utf8
from collections import defaultdict

def nonterminal_representer(dumper, data):
    return dumper.represent_scalar("!nonterminal", data)

class Nonterminal(object):
    __nonterminals = defaultdict(int)

    def __init__(self, terminal):
        self.__nonterminal = terminal
        type(self).__nonterminals[self] += 1

    @property
    def nonterminal(self):
        return self.__nonterminal

    def __repr__(self):
        return self.__nonterminal

    def __str__(self):
        return repr(self)

    def __len__(self):
        return 1

    def __eq__(self, other):
        if self.__nonterminal == other.nonterminal:
            return True
        return False

    def __hash__(self):
        return 1

    @staticmethod
    def getnonterminals(key=None):
        if key is not None:
            return Nonterminal.__nonterminals[key]
        else:
            return Nonterminal.__nonterminals

if __name__ == '__main__':
    import yaml
    from yaml.representer import Representer

    Representer.add_representer(Nonterminal, nonterminal_representer)
    x = Nonterminal("X")
    y = Nonterminal("X")
    print(yaml.dump(x))
