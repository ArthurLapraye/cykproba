# coding: utf8

from Nonterminal import Nonterminal
from Terminal import Terminal
import productions




# extraire une grammaire hors contexte probabilisee
# soit appliquer calculproba sur


class Grammaire(object):
    def __init__(self, terminals, nonterminals, axiome, productions):
        """
        
        :param terminals:
        :param nonterminals:
        :param axiome:
        :param productions:
        :return: None
        """
        if all(isinstance(t, Terminal) for t in terminals):
            self.__terminals = terminals
        else:
            raise TypeError("L'alphabet terminal ne doit être composé que de Terminal")

        if all(isinstance(nt, Nonterminal) for nt in nonterminals):
            self.__nonterminals = nonterminals
        else:
            raise TypeError("l'alphabet nonterminal ne doit être composé que de Nonterminal")

        if axiome in nonterminals:
            self.__axiome = axiome
        else:
            raise TypeError("L'axiome doit nécessairement faire partie de l'ensemble nonterminals")

        if all(isinstance(prod, productions.Production) for prod in productions):
            self.__productions = productions
        else:
            raise TypeError("Les productions doivent être composées de Production")

    @property
    def terminals(self):
        return self.__terminals

    @property
    def nonterminals(self):
        return self.__nonterminals

    @property
    def axiome(self):
        return self.__axiome

    @property
    def productions(self):
        return self.__productions

    def __repr__(self):
        return

    def __str__(self):
        return repr(self)


class GrammaireHorsContexte(Grammaire):
    def __init__(self, terminals, nonterminals, axiome, prods):
        Grammaire.__init__(self, terminals, nonterminals, axiome, productions)
        if all(isinstance(prod.lhs, productions.ProductionHorsContexte) for prod in prods):
            self.__productions = prods
        else:
            raise TypeError("Une grammaire hors-contexte peut contenir des productions unaires, binaires, lexicales ou encore n-aires")

    def GrammaireHorsContexte2GrammaireHorsContexteCNF(self):
        terminals = set()
        nonterminals = set()
        axiome = set()
        productions = set()

        def unarise(productionsHorsContexteUnaires):
            pass
        def binarise(productionsHorsContexteNaires):
            pass
        return GrammaireHorsContexteCNF(terminals, nonterminals, axiome, productions)


class GrammaireHorsContexteCNF(GrammaireHorsContexte):
    def __init__(self, terminals, nonterminals, axiome, prods):
        GrammaireHorsContexte.__init__(self, terminals, nonterminals, axiome, prods)
        if all(
            isinstance(
                x,
                (
                    productions.ProductionHorsContexteBinaire,
                    productions.ProductionHorsContexteLexicale
                )
            ) for x in prods
        ):
            self.__productions = prods
        else:
            raise TypeError("""
                Une grammaire hors-contexte en forme normale de Chomsky ne peut contenir
                que des productions de la forme binaire ou lexicale
            """)


class GrammaireHorsContexteCNFProbabilisee(GrammaireHorsContexteCNF):
    def __init__(self, terminals, nonterminals, axiome, prods):
        GrammaireHorsContexteCNF.__init__(self, terminals, nonterminals, axiome, prods)
        if all(
            isinstance(
                x,
                (
                    productions.ProductionHorsContexteBinaireProbabilisee,
                    productions.ProductionHorsContexteLexicaleProbabilisee
                )
            ) for x in prods
        ):
            self.__productions = prods
        else:
            raise TypeError("""
                Une grammaire hors-contexte probabilisee en forme normale de Chomsky ne peut contenir
                que des productions de la forme binaire ou lexicale et une probabilité associée à chaque règle
                """)


class GrammaireHorsContexteProbabilisee(GrammaireHorsContexte):
    def __init__(self, terminals, nonterminals, axiome, prods):
        GrammaireHorsContexte.__init__(self, terminals, nonterminals, axiome, prods)
        if all(isinstance(x, productions.ProductionHorsContexteProbabilisee) for x in prods):
            self.__prductions = prods
        else:
            raise TypeError(
                """Une grammaire hors-contexte probabilisee doit contenir des ProductionHorsContexteProbabilisee"""
            )

    def GrammaireHorsContexteProbabilisee2GrammaireHorsContexteCNFProbabilisee(self):
        terminals = set()
        nonterminals = set()
        axiome = set()
        productions = set()

        self.calculProba()
        self.ununarise()
        self.binarise()

        return GrammaireHorsContexteCNFProbabilisee(terminals, nonterminals, axiome, productions)

    def calculProba(self, productionsHorsContexteProbabilisees):
        # temp = groupby(lhs)
        # x.proba /= len(nt) for x in nt for nt in temp
        # si prod1 == prod2:
            # prod1.proba += prod2.proba
            # del prod2
        #
        pass
    def ununarise(self, productionsHorsContexteUnairesProbabilisees):
        for unary in productionsHorsContexteUnairesProbabilisees:

        # pour chaque regle unaire:
            # 1 - ajouter un nouveau nouveau nonterminal
            # 2 - del regle unaire
            # 3 - pour chaque regle n-aire dont la partie droite de la regle unaire est contenu dans la partie droite de la regle n-aire
                # - ajouter une prod avec nouveau nonterminal, proba p1*p2
                # - fixer à l'ancienne prod p2*(1-p1)
            # 4 - pour chaque production lexicale avec partie gauche de regle unaire dans partie gauche de prod lexicale
                # - fixer proba à p3/(1 - p1)
            # 5 - pour chaque prod lexicale avec partie droite de regle unaire en lhs
                # - proba de la nouvelle regle == proba de l'ancienne
        pass
    def binarise(self, productionsHorsContexteNairesProbabilisees):
        # - ajouter nonterminal jusqu'à n-1 séparateur '-'
        # - ajouter regle binaire à productions avec même proba
        # - si la regle est binaire:
            # ajouter la prudction à productions, avec proba de 1
        # - sinon:
            # binarise(regle)
        # -
        pass




if __name__ == '__main__':
    productions.Production(Nonterminal("X"), Terminal("x"))
    productions.Production(Nonterminal("Y"), [Nonterminal("X"), Nonterminal("Z")])
    productions.Production(Nonterminal("Z"), Terminal("z"))
    terminals = Terminal
    nonterminals = Nonterminal
    axiome = Nonterminal("Y")
    productions = productions.Production
    print()
