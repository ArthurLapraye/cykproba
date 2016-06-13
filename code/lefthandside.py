# coding: utf8
import handside
import nonterminal


def lefthandside_representer(dumper, data):
    return dumper.represent_sequence("!left-handside", data)


def lefthandside1_representer(dumper, data):
    return dumper.represent_sequence("!left-hanside-1", data)


def lefthandsidehorscontexte_representer(dumper, data):
    return dumper.represent_sequence("!left-handside-hors-contexte", data)





class Lefthandside(handside.Handside):
    def __init__(self, *args):
        super(Lefthandside, self).__init__(*args)
        self.check_length(1, args, ">=")

    def __eq__(self, other):
        if self.__dict__ == other.__dict__:
            return True
        return False

    def __hash__(self): return 0

class Lefthandside1(Lefthandside):
    def __init__(self, *args):
        super(Lefthandside1, self).__init__(*args)
        self.check_length(1, args, "==")

    def __eq__(self, other):
        if self.__dict__ == other.__dict__:
            return True
        return False

    def __hash__(self): return 0

class Lefthandsidehorscontexte(Lefthandside1):
    def __init__(self, *args):
        super(Lefthandsidehorscontexte, self).__init__(*args)
        self.check_type(args, nonterminal.Nonterminal)

    def __eq__(self, other):
        if self.__dict__ == other.__dict__:
            return True
        return False

    def __hash__(self): return 0

if __name__ == '__main__':
    x = Lefthandside(nonterminal.Nonterminal('T'), nonterminal.Nonterminal('Y'))
