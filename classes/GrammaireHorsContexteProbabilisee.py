# coding: utf8

from GrammaireHorsContexte import GrammaireHorsContexte
from GrammaireHorsContexteCNFProbabilisee import GrammaireHorsContexteCNFProbabilisee
from ProductionHorsContexteUnaireProbabilisee import ProductionHorsContexteUnaireProbabilisee
from ProductionHorsContexteBinaireProbabilisee import ProductionHorsContexteBinaireProbabilisee
from ProductionHorsContexteLexicaleProbabilisee import ProductionHorsContexteLexicaleProbabilisee
from ProductionHorsContexteNaireProbabilisee import ProductionHorsContexteNaireProbabilisee


class GrammaireHorsContexteProbabilisee(GrammaireHorsContexte):
    def __init__(self, terminals, nonterminals, axiome, productionsHorsContextesProbabilisees):
        GrammaireHorsContexte.__init__(self, terminals, nonterminals, axiome, productionsHorsContextesProbabilisees)
        assert all(
            isinstance(
                x,
                (
                    ProductionHorsContexteUnaireProbabilisee,
                    ProductionHorsContexteBinaireProbabilisee,
                    ProductionHorsContexteLexicaleProbabilisee,
                    ProductionHorsContexteNaireProbabilisee
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
        def ununarise(productionsHorsContexteUnairesProbabilisees):
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