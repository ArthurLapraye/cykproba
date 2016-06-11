# coding: utf8
import terminal
import nonterminal
import collections
import errors


def handside_representer(dumper, data):
    return dumper.represent_sequence("!handside", data)


class Handside(collections.Sequence):
    """
        Inspirée de ce lien:
        source : http://stackoverflow.com/questions/3487434/overriding-append-method-after-inheriting-from-a-python-list
    """

    def __init__(self, *args):
        self.__list = list(args)
        self.check_type(args, (nonterminal.Nonterminal, terminal.Terminal))
        self.check_length(0, args, ">=")

    @property
    def list(self):
        return self.__list

    def check_type(self, iterable, *types):
        if not all(isinstance(x, types) for x in iterable):
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

    def __eq__(self, other):
        if self.__dict__ == other.__dict__:
            return True
        return False

    def __hash__(self): return 1

    def __len__(self): return len(self.__list)

    def __getitem__(self, i): return self.__list[i]

    def __repr__(self): return str(self.__list)

    def __str__(self): return repr(self)


if __name__ == '__main__':
    pass
