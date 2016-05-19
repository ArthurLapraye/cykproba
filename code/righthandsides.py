# coding: utf8

from nonterminal import Nonterminal
from terminal import Terminal
from handside import Handside


class LengthError(LookupError):
    """Vérification de la longueur d'un iterable"""


class Righthandside(Handside):
    def __init__(self, args):
        if not all(isinstance(x, (Terminal, Nonterminal)) for x in args):
            raise TypeError('une Righthandside peut etre composé de Terminal ou de Nonterminal')
        else:
            super(Righthandside, self).__init__(args)
            self.__rhs = args

    def __repr__(self):
        return " ".join([str(x) for x in self.__rhs])

    def __str__(self):
        return repr(self)

    def __len__(self):
        return len(self.__rhs)

    def __eq__(self, other):
        if self.__rhs == other.rhs:
            return True
        else:
            return False

#    def __getitem__(self, item):
#        return self.__rhs[item]

    @property
    def rhs(self):
        return self.__rhs

#    @rhs.setter
#    def rhs(self, value):
#        pass

    def replace(self, old, new):
        print(self.rhs)
        x = self.rhs.index(old)
        print(x)
        #return Righthandside(self.__rhs[:x] + new + self.__rhs[x+1:])


class Righthandside0(Righthandside):
    pass


class Righthandside1(Righthandside):
    def __init__(self, args):
        if len(args) != 1:
            raise LengthError("Une Righthandside1 ne doit contenir qu'un seul élément.")
        else:
            super(Righthandside1, self).__init__(args)

    def replace(self, old, new):
        x = self.rhs.index(old)
        return Righthandside1(self.rhs[:x] + [new] + self.rhs[x+1:])


class Righthandside2(Righthandside):
    def __init__(self, args):
        if len(args) != 2:
            raise LengthError("Une Righthandside2 ne doit contenir que deux éléments.")
        else:
            super(Righthandside2, self).__init__(args)

    def replace(self, old, new):
        x = self.rhs.index(old)
        return Righthandside2(self.rhs[:x] + (new, ) + self.rhs[x+1:])


class RighthandsideN(Righthandside):
    def __init__(self, args):
        if len(args) < 2:
            raise LengthError('Une RighthandsideN ne doit pas contenir en dessous de deux éléments')
        else:
            super(RighthandsideN, self).__init__(args)

    def replace(self, old, new):
        x = self.rhs.index(old)
        return RighthandsideN(self.rhs[:x] + (new, ) + self.rhs[x+1:])


class Righthandside1unaire(Righthandside1):
    def __init__(self, args):
        if not all(isinstance(x, Nonterminal) for x in args):
            raise TypeError("Le seul élément d'une Righthandside1unaire doit être de type Nonterminal.")
        else:
            super(Righthandside1unaire, self).__init__(args)

    def replace(self, old, new):
        x = self.rhs.index(old)
        return Righthandside1unaire(self.rhs[:x] + (new, ) + self.rhs[x+1:])


class Righthandside1lexicale(Righthandside1):
    def __init__(self, args):
        if not all(isinstance(x, Terminal) for x in args):
            raise TypeError("Le seul élément d'une Righthandside1lexicale doit être de type Terminal.")
        else:
            super(Righthandside1lexicale, self).__init__(args)

    def replace(self, old, new):
        x = self.rhs.index(old)
        return Righthandside1lexicale(self.rhs[:x] + (new, ) + self.rhs[x+1:])


class Righthandside2binaire(Righthandside2):
    def __init__(self, args):
        if not all(isinstance(x, Nonterminal) for x in args):
            raise LengthError("Les deux éléments d'une Righthandside2binaire doivent être de type Nonterminal.")
        else:
            super(Righthandside2binaire, self).__init__(args)

    def replace(self, old, new):
        x = self.rhs.index(old)
        return Righthandside2binaire(self.rhs[:x] + (new,) + self.rhs[x+1:])


class RighthandsideNaire(RighthandsideN):
    def __init__(self, args):
        if not all(issubclass(type(x), Nonterminal) for x in args):
            raise TypeError('Tous les éléments d\'une RighthandsideNaire doivent être des Nonterminal')
        else:
            super(RighthandsideNaire, self).__init__(args)

    def replace(self, old, new):
        x = self.rhs.index(old)
        return RighthandsideNaire(self.rhs[:x] + (new,) + self.rhs[x+1:])


if __name__ == '__main__':
    x = Righthandside((Nonterminal("X"), Nonterminal("Y"), Terminal("ont")))
    y = Righthandside((Nonterminal('Y'), Nonterminal("Z")))
    print(x|y)
