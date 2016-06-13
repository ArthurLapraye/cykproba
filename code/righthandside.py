# coding: utf8
import terminal
import nonterminal
import handside

#
# def righthandside_representer(dumper, data):
#     return dumper.represent_sequence("!righthandside", data)
#
#
# def righthandside1_representer(dumper, data):
#     return dumper.represent_sequence("!righthandside1", data)
#
#
# def righthandside2_representer(dumper, data):
#     return dumper.represent_sequence("!righthandside2", data)
#
#
# def righthandsideN_representer(dumper, data):
#     return dumper.represent_sequence("!righthandsideN", data)
#
#
# def righthandside1unaire_representer(dumper, data):
#     return dumper.represent_sequence("!righthandside1unaire", data)
#
#
# def righthandside1lexicale_representer(dumper, data):
#     return dumper.represent_sequence("!righthandside1lexicale", data)
#
#
# def righthandside2binaire_representer(dumper, data):
#     return dumper.represent_sequence("!righthandside2binaire", data)
#
#
# def righthandsideNaire_representer(dumper, data):
#     return dumper.represent_sequence("!righthandsideNaire", data)


class Righthandside(handside.Handside):
    def __init__(self, *args):
        super(Righthandside, self).__init__(*args)

    def __eq__(self, other):
        if self.__dict__ == other.__dict__:
            return True
        return False

    def __hash__(self): return 0


class Righthandside1(Righthandside):
    def __init__(self, *args):
        super(Righthandside1, self).__init__(*args)
        self.check_length(1, args, "==")

    def __eq__(self, other):
        if self.__dict__ == other.__dict__:
            return True
        return False

    def __hash__(self): return 0


class Righthandside2(Righthandside):
    def __init__(self, *args):
        super(Righthandside2, self).__init__(*args)
        self.check_length(2, args, "==")

    def __eq__(self, other):
        if self.__dict__ == other.__dict__:
            return True
        return False

    def __hash__(self): return 0


class RighthandsideNaire(Righthandside):
    def __init__(self, *args):
        super(RighthandsideNaire, self).__init__(*args)
        self.check_length(2, args, ">")

    def __eq__(self, other):
        if self.__dict__ == other.__dict__:
            return True
        return False

    def __hash__(self): return 0


class Righthandside1unaire(Righthandside1):
    def __init__(self, *args):
        super(Righthandside1unaire, self).__init__(*args)
        self.check_type(args, nonterminal.Nonterminal)

    def __eq__(self, other):
        if self.__dict__ == other.__dict__:
            return True
        return False

    def __hash__(self): return 0


class Righthandside1lexicale(Righthandside1):
    def __init__(self, *args):
        super(Righthandside1lexicale, self).__init__(*args)
        self.check_type(args, terminal.Terminal)

    def __eq__(self, other):
        if self.__dict__ == other.__dict__:
            return True
        return False

    def __hash__(self): return 0


class Righthandside2binaire(Righthandside2):
    def __init__(self, *args):
        super(Righthandside2binaire, self).__init__(*args)
        self.check_type(args, nonterminal.Nonterminal)

    def __eq__(self, other):
        if self.__dict__ == other.__dict__:
            return True
        return False

    def __hash__(self): return 0

if __name__ == '__main__':
    pass
