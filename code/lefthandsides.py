# coding: utf8

from terminal import Terminal
from nonterminal import Nonterminal


class Lefthandside(object):
    """
        classe abstraite disant qu'il y a un attribut d'instance lhs mais sans restriction mais
        tout en ayant les propriétés d'une lhs soit présant dans (X U V)* V (X U V)*
    """
    def __init__(self, lhs):
        """

        :param lhs: iterable de (Terminal U Nonterminal)* Nonterminal (Terminal U Nonterminal)*
        :return: None
        """
        if not (((len(lhs) == 1) and isinstance(lhs, Nonterminal)) or ((len(lhs) > 1) and all(isinstance(x, (Nonterminal, Terminal)) for x in lhs))):
            raise TypeError(
                "La partie gauche doit soit être un Nonterminal ou bien une suite de terminaux/nonterminaux"
            )
        else:
            self.__lhs = lhs

    def __repr__(self):
        return "".join([str(x) for x in self.__lhs])

    def __str__(self):
        return repr(self)


class LefthandsideHorsContexte(Lefthandside):
    """
        Restriction sur le type de l'attribut d'instance lhs
    """
    def __init__(self, lhs):
        """

        :param lhs: Nonterminal
        :return: None
        """
        if not ((len(lhs) == 1) and isinstance(lhs, Nonterminal)):
            raise TypeError('En hors-contexte, la partie gauche doit être un Nonterminal. %s' % type(lhs).__name__)
        else:
            self._Lefthandside__lhs = lhs


if __name__ == '__main__':
    x = Lefthandside([Nonterminal("X"), Terminal('ons')])
    print(x)
    y = LefthandsideHorsContexte(Nonterminal('X'))
    print(y)
