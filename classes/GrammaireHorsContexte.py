# coding: utf8

from Grammaire import Grammaire
from GrammaireHorsContexteCNF import GrammaireHorsContexteCNF
from ProductionHorsContexteUnaire import ProductionHorsContexteUnaire
from ProductionHorsContexteBinaire import ProductionHorsContexteBinaire
from ProductionHorsContexteLexicale import ProductionHorsContexteLexicale
from ProductionHorsContexteNaire import ProductionHorsContexteNaire




class GrammaireHorsContexte(Grammaire):
    def __init__(self, terminals, nonterminals, axiome, productionsHorsContexte):
        Grammaire.__init__(self, terminals, nonterminals, axiome, productionsHorsContexte)
        assert all(
            isinstance(
                x,
                (
                    ProductionHorsContexteUnaire,
                    ProductionHorsContexteBinaire,
                    ProductionHorsContexteLexicale,
                    ProductionHorsContexteNaire
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