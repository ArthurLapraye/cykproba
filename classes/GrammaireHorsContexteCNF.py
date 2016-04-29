# coding: utf8

from GrammaireHorsContexte import GrammaireHorsContexte
from ProductionHorsContexteBinaire import ProductionHorsContexteBinaire
from ProductionHorsContexteLexicale import ProductionHorsContexteLexicale




class GrammaireHorsContexteCNF(GrammaireHorsContexte):
    def __init__(self, terminals, nonterminals, axiome, productionsHorsContexte):
        GrammaireHorsContexte.__init__(self, terminals, nonterminals, axiome, productionsHorsContexte)
        assert all(
            isinstance(
                x,
                (
                    ProductionHorsContexteBinaire,
                    ProductionHorsContexteLexicale
                )
            ) for x in productionsHorsContexte
        ), """
            Une grammaire hors-contexte en forme normale de Chomsky ne peut contenir
            que des productions de la forme binaire ou lexicale
        """
