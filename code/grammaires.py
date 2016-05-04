# coding: utf8

from Nonterminal import Nonterminal
from Terminal import Terminal
import productions


class Grammaire(object):
    def __init__(self, terminals, nonterminals, axiome, productions):
        """
        
        :param terminals:
        :param nonterminals:
        :param axiome:
        :param productions:
        :return:
        """
        assert isinstance(terminals, set) and all(isinstance(x, Terminal) for x in terminals), "L'alphabet terminal ne doit être composé que de terminaux"
        assert isinstance(nonterminals, set) and all(isinstance(x, Nonterminal) for x in nonterminals), "l'alphabet nonterminal ne doit être composé que de nonterminaux"
        assert isinstance(axiome, Nonterminal) and (axiome in nonterminals), "L'axiome doit nécessairement faire partie de l'ensemble nonterminals"
        assert isinstance(productions, set), "Les productions doivent être encapsulées dans un set"
        self.terminals = terminals
        self.nonterminals = nonterminals
        self.axiome = axiome
        self.productions = productions

    def __repr__(self):
        return

    def __str__(self):
        return repr(self)


class GrammaireHorsContexte(Grammaire):
    def __init__(self, terminals, nonterminals, axiome, productionsHorsContexte):
        Grammaire.__init__(self, terminals, nonterminals, axiome, productionsHorsContexte)
        assert all(
            isinstance(
                x,
                (
                    productions.ProductionHorsContexteUnaire,
                    productions.ProductionHorsContexteBinaire,
                    productions.ProductionHorsContexteLexicale,
                    productions.ProductionHorsContexteNaire
                )
            ) for x in productionsHorsContexte
        ), "Une grammaire hors-contexte peut contenir des productions unaires, binaires, lexicales ou encore n-aires"

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
    def __init__(self, terminals, nonterminals, axiome, productionsHorsContexte):
        GrammaireHorsContexte.__init__(self, terminals, nonterminals, axiome, productionsHorsContexte)
        assert all(
            isinstance(
                x,
                (
                    productions.ProductionHorsContexteBinaire,
                    productions.ProductionHorsContexteLexicale
                )
            ) for x in productionsHorsContexte
        ), """
            Une grammaire hors-contexte en forme normale de Chomsky ne peut contenir
            que des productions de la forme binaire ou lexicale
        """


class GrammaireHorsContexteCNFProbabilisee(GrammaireHorsContexteCNF):
    def __init__(self, terminals, nonterminals, axiome, productionsHorsContexte):
        GrammaireHorsContexteCNF.__init__(self, terminals, nonterminals, axiome, productionsHorsContexte)
        assert all(
            isinstance(
                x,
                (
                    productions.ProductionHorsContexteBinaireProbabilisee,
                    productions.ProductionHorsContexteLexicaleProbabilisee
                )
            ) for x in productionsHorsContexte
        ), """
            Une grammaire hors-contexte probabilisee en forme normale de Chomsky ne peut contenir
            que des productions de la forme binaire ou lexicale et une probabilité associée à chaque règle
        """


class GrammaireHorsContexteProbabilisee(GrammaireHorsContexte):
    def __init__(self, terminals, nonterminals, axiome, productionsHorsContextesProbabilisees):
        GrammaireHorsContexte.__init__(self, terminals, nonterminals, axiome, productionsHorsContextesProbabilisees)
        assert all(
            isinstance(
                x,
                (
                    productions.ProductionHorsContexteUnaireProbabilisee,
                    productions.ProductionHorsContexteBinaireProbabilisee,
                    productions.ProductionHorsContexteLexicaleProbabilisee,
                    productions.ProductionHorsContexteNaireProbabilisee
                )
            ) for x in productionsHorsContextesProbabilisees
        ), """
                Une grammaire hors-contexte probabilisee peut contenir
                des productions unaires, binaires, lexicales ou encore n-aires mais avec une probabilité
        """

    def GrammaireHorsContexteProbabilisee2GrammaireHorsContexteCNFProbabilisee(self):
        terminals = set()
        nonterminals = set()
        axiome = set()
        productions = set()

        def calculProba(productionsHorsContexteProbabilisees):
            # temp = groupby(lhs)
            # x.proba /= len(nt) for x in nt for nt in temp
            # si prod1 == prod2:
                # prod1.proba += prod2.proba
                # del prod2
            #
            pass
        def ununarise(productionsHorsContexteUnairesProbabilisees):
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
        def binarise(productionsHorsContexteNairesProbabilisees):
            # - ajouter nonterminal jusqu'à n-1 séparateur '-'
            # - ajouter regle binaire à productions avec même proba
            # - si la regle est binaire:
                # ajouter la prudction à productions, avec proba de 1
            # - sinon:
                # binarise(regle)
            # -
            pass
        return GrammaireHorsContexteCNFProbabilisee(terminals, nonterminals, axiome, productions)






