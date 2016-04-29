# coding: utf8

from GrammaireHorsContexteCNF import GrammaireHorsContexteCNF
from ProductionHorsContexteLexicaleProbabilisee import ProductionHorsContexteLexicaleProbabilisee
from ProductionHorsContexteBinaireProbabilisee import ProductionHorsContexteBinaireProbabilisee



class GrammaireHorsContexteCNFProbabilisee(GrammaireHorsContexteCNF):
    def __init__(self, terminals, nonterminals, axiome, productionsHorsContexte):
        GrammaireHorsContexteCNF.__init__(self, terminals, nonterminals, axiome, productionsHorsContexte)
        assert all(
            isinstance(
                x,
                (
                    ProductionHorsContexteBinaireProbabilisee,
                    ProductionHorsContexteLexicaleProbabilisee
                )
            ) for x in productionsHorsContexte
        ), """
            Une grammaire hors-contexte probabilisee en forme normale de Chomsky ne peut contenir
            que des productions de la forme binaire ou lexicale et une probabilité associée à chaque règle
        """