# coding: utf8

import lefthandside
import righthandside
import fractions
import collections
import errors


def production_representer(dumper, data):
    return dumper.represent_set("!production", str(data))


def productionhorscontexte_representer(dumper, data):
    return dumper.represent_scalar("!production-hors-contexte", str(data))


def productionhorscontexteprobabilisee_representer(dumper, data):
    return dumper.represent_scalar("!production-hors-contexte-probabilisee", str(data))


def productionhorscontexte1_representer(dumper, data):
    return dumper.represent_scalar("!production-hors-contexte-1", str(data))


def productionhorscontexte1probabilisee_representer(dumper, data):
    return dumper.represent_scalar("!production-hors-contexte-1-probabilisee", str(data))


def productionhorscontexte1unaire_representer(dumper, data):
    return dumper.represent_scalar("!production-hors-contexte-1-unaire", str(data))


def productionhorscontexte1unaireprobabilisee_representer(dumper, data):
    return dumper.represent_scalar("!production-hors-contexte-1-unaire-probabilisee", str(data))


def Productionhorscontexte1lexicale_representer(dumper, data):
    return dumper.represent_scalar("!Production-hors-contexte-1-lexicale", str(data))


def Productionhorscontexte1lexicaleprobabilisee_representer(dumper, data):
    return dumper.represent_scalar("!Production-hors-contexte-1-lexicale-probabilisee", str(data))


def Productionhorscontexte2_representer(dumper, data):
    return dumper.represent_scalar("!Production-hors-contexte-2", str(data))


def Productionhorscontexte2probabilisee_representer(dumper, data):
    return dumper.represent_scalar("!Production-hors-contexte-2-probabilisee", str(data))


def Productionhorscontexte2binaire_representer(dumper, data):
    return dumper.represent_scalar("!Production-hors-contexte-2-binaire", str(data))


def Productionhorscontexte2binaireprobabilisee_representer(dumper, data):
    return dumper.represent_scalar("!Production-hors-contexte-2-binaire-probabilisee", str(data))


def Productionhorscontextenaire_representer(dumper, data):
    return dumper.represent_scalar("!Production-hors-contexte-n-aire", str(data))


def Productionhorscontextenaireprobabilisee_representer(dumper, data):
    return dumper.represent_scalar("!Production-hors-contexte-n-aire-probabilisee", str(data))


class Production(collections.Sequence):
    __productions = collections.defaultdict(int)
    __lefthandsides = collections.defaultdict(int)

    def __init__(self, *args):
        self.__list = list(args)
        self.check_type(args, (lefthandside.Lefthandside, righthandside.Righthandside))
        self.check_length(2, args, "==")

        self.__productions[self] += 1
        self.__lefthandsides[self[0]] += 1

    @property
    def list(self):
        return self.__list

    def check_type(self, iterable, *types):

        if not all(isinstance(*x) for x in zip(iterable, types)):
            raise TypeError(
                'Une {name} doit être une séquence de: {types}'.format(
                    name=self.__class__.__name__,
                    types=" et/ou ".join([x.__name__ for x in types])
                )
            )

    def check_length(self, i, iterable, equation="=="):
        if equation == "==":
            if not (len(iterable) == i):
                raise errors.LengthError(
                    'Une {name} doit faire {equation} {i} élément(s)'.format(
                        name=self.__class__.__name__, i=i, equation=equation
                    )
                )
        elif equation == "<=":
            if not (len(iterable) <= i):
                raise errors.LengthError(
                    'Une {name} doit faire {equation} {i} élément(s)'.format(
                        name=self.__class__.__name__, i=i, equation=equation
                    )
                )
        elif equation == ">=":
            if not (len(iterable) >= i):
                raise errors.LengthError(
                    'Une {name} doit faire {equation} {i} élément(s)'.format(
                        name=self.__class__.__name__, i=i, equation=equation
                    )
                )
        elif equation == "!=":
            if not (len(iterable) != i):
                raise errors.LengthError(
                    'Une {name} doit faire {i} {equation} élément(s)'.format(
                        name=self.__class__.__name__, i=i, equation=equation
                    )
                )
        elif equation == ">":
            if not (len(iterable) > i):
                raise errors.LengthError(
                    'Une {name} doit faire {i} {equation} élément(s)'.format(
                        name=self.__class__.__name__, i=i, equation=equation
                    )
                )
        elif equation == "<":
            if not (len(iterable) < i):
                raise errors.LengthError(
                    'Une {name} doit faire {i} {equation} élément(s)'.format(
                        name=self.__class__.__name__, i=i, equation=equation
                    )
                )

    def replace(self, types, old, new):
        copie = self.__list.copy()
        if old in self.__list:
            ind = copie.index(old)
            copie.remove(old)
            copie.insert(ind, new)
            return type(self)(types, *copie)
        else:
            return type(self)(types, copie)

    @staticmethod
    def productions():
        return Production.__productions

    @staticmethod
    def lefthandsides():
        return Production.__lefthandsides

    @staticmethod
    def subset_productions(productions, cls, nt=None):
        if nt is None:
            return [x for x in productions if issubclass(type(x), cls)]
        else:
            return [x for x in productions if issubclass(type(x), cls) and (x.lhs.lhs[0] == nt)]

    @staticmethod
    def setprobaproductions():
        for p in Production.productions():
            p.setproba()

    def __eq__(self, other):
        if self.__dict__ == other.__dict__:
            return True
        return False

    def __hash__(self): return 0

    def __len__(self): return len(self.__list)

    def __getitem__(self, i): return self.__list[i]

    def __repr__(self): return " > ".join([str(x) for x in self.__list])

    def __str__(self): return repr(self)


class Productionhorscontexte(Production):
    def __init__(self, *args):
        super(Productionhorscontexte, self).__init__(*args)
        self.check_type(args, lefthandside.Lefthandsidehorscontexte, righthandside.Righthandside)


class Productionhorscontexteprobabilisee(Productionhorscontexte):
    def __init__(self, *args):
        super(Productionhorscontexteprobabilisee, self).__init__(*args)
        self.__proba = fractions.Fraction(1, 1)

    @property
    def proba(self):
        return self.__proba

    @proba.setter
    def proba(self, value):
        self.__proba = value

    def setproba(self):
        self.proba = fractions.Fraction(self.productions()[self], self.lefthandsides()[self[0]])


class Productionhorscontexte1(Productionhorscontexte):
    def __init__(self, *args):
        super(Productionhorscontexte1, self).__init__(*args)
        self.check_type(args, lefthandside.Lefthandsidehorscontexte, righthandside.Righthandside1)


class Productionhorscontexte1probabilisee(Productionhorscontexte1):
    def __init__(self, *args):
        super(Productionhorscontexte1probabilisee, self).__init__(*args)
        self.__proba = fractions.Fraction(1, 1)

    @property
    def proba(self):
        return self.__proba

    @proba.setter
    def proba(self, value):
        self.__proba = value

    def setproba(self):
        self.__proba = fractions.Fraction(self.productions()[self], self.lefthandsides()[self[0]])


class Productionhorscontexte1unaire(Productionhorscontexte1):
    def __init__(self, *args):
        super(Productionhorscontexte1unaire, self).__init__(*args)
        self.check_type(args, lefthandside.Lefthandsidehorscontexte, righthandside.Righthandside1unaire)


class Productionhorscontexte1unaireprobabilisee(Productionhorscontexte1unaire):
    def __init__(self, *args):
        super(Productionhorscontexte1unaireprobabilisee, self).__init__(*args)
        self.__proba = fractions.Fraction(1, 1)

    @property
    def proba(self):
        return self.__proba

    @proba.setter
    def proba(self, value):
        self.__proba = value

    def setproba(self):
        self.__proba = fractions.Fraction(self.productions()[self], self.lefthandsides()[self[0]])


class Productionhorscontexte1lexicale(Productionhorscontexte1):
    def __init__(self, *args):
        super(Productionhorscontexte1lexicale, self).__init__(*args)
        self.check_type(args, lefthandside.Lefthandsidehorscontexte, righthandside.Righthandside1lexicale)


class Productionhorscontexte1lexicaleprobabilisee(Productionhorscontexte1lexicale):
    def __init__(self, *args):
        super(Productionhorscontexte1lexicaleprobabilisee, self).__init__(*args)
        self.__proba = fractions.Fraction(1, 1)

    @property
    def proba(self):
        return self.__proba

    @proba.setter
    def proba(self, value):
        self.__proba = value

    def setproba(self):
        self.__proba = fractions.Fraction(self.productions()[self], self.lefthandsides()[self[0]])


class Productionhorscontexte2(Productionhorscontexte):
    def __init__(self, *args):
        super(Productionhorscontexte2, self).__init__(*args)
        self.check_type(args, lefthandside.Lefthandsidehorscontexte, righthandside.Righthandside2)


class Productionhorscontexte2binaire(Productionhorscontexte2):
    def __init__(self, *args):
        super(Productionhorscontexte2binaire, self).__init__(*args)
        self.check_type(args, lefthandside.Lefthandsidehorscontexte, righthandside.Righthandside2binaire)


class Productionhorscontexte2binaireprobabilisee(Productionhorscontexte2binaire):
    def __init__(self, *args):
        super(Productionhorscontexte2binaireprobabilisee, self).__init__(*args)
        self.__proba = fractions.Fraction(1, 1)

    @property
    def proba(self):
        return self.__proba

    @proba.setter
    def proba(self, value):
        self.__proba = value

    def setproba(self):
        self.__proba = fractions.Fraction(self.productions()[self], self.lefthandsides()[self[0]])


class ProductionhorscontexteNaire(Productionhorscontexte):
    def __init__(self, *args):
        super(ProductionhorscontexteNaire, self).__init__(*args)
        self.check_type(args, lefthandside.Lefthandsidehorscontexte, righthandside.RighthandsideNaire)


class ProductionhorscontexteNaireprobabilisee(ProductionhorscontexteNaire):
    def __init__(self, *args):
        super(ProductionhorscontexteNaireprobabilisee, self).__init__(*args)
        self.__proba = fractions.Fraction(1, 1)

    @property
    def proba(self):
        return self.__proba

    @proba.setter
    def proba(self, value):
        self.__proba = value

    def setproba(self):
        self.__proba = fractions.Fraction(self.productions()[self], self.lefthandsides()[self[0]])


if __name__ == '__main__':
    pass
