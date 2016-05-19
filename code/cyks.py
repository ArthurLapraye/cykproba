#coding: utf8
from collections import defaultdict
from cellules import *
from grammaires import *


class CKY(object):
    def __init__(self):
        self.chart = defaultdict(list)

    def get_axiome(self, phrase):
        return (len(phrase), 0)

    def initialise(self, phrase):
        s = next(self.span)
        for (t, mot) in enumerate(iterable=phrase, start=1):
            x = t-1
            for lexical in [x for x in self.grammaire.getproductionshorscontextesbinaires()]:
                pass

    def load_grammaire(self, grammaire):
        """

        :param grammaire: grammaire hors contexte sous forme normale de Chomsky
        :type grammaire: GrammaireHorsContexteCNF
        :return: None
        """
        if not issubclass(type(grammaire), Grammairehorscontextecnf):
            raise TypeError('CKY ne peut fonctionner qu\'avec une grammaire hors contexte mise sous forme normale de chomsky')
        else:
            self.grammaire = grammaire

    def remplit(self, phrase):
        pass

    def get_arbre(self, phrase, i):
        pass

    def get_foret(self, phrase):
        pass

    def predit(self, phrase):
        """

        :param phrase:
        :return:
        """
        self.span = (x for x, y in enumerate(range(len(phrase)),start=1))
        self.initialise(phrase)
        self.remplit(phrase)


class CKYP(CKY):
    """

    """
    def initialise(self, phrase):
        """

        :param phrase:
        :return:
        """
        s = next(self.span)
        for (t, mot) in enumerate(iterable=phrase, start=1):
            x = t-1
            for lexical in self.grammaire.getproductionshorscontextesprobabiliseeslexicales():
                r = len(self.chart[(x, s)])+1
                self.chart[(x, s)] |= Celluleproba(
                                    lhs=lexical.lhs,
                                    proba=lexical.proba,
                                    backpointer=None,
                                    index=r
                                )

    def remplit(self, phrase):
        """

        :param phrase:
        :return:
        """
        for s in self.span:
            for t in range(len(phrase)-s+1):
                x = t-1
                for m in range(t, t+s-2):
                    p = m-x
                    q = s-p
                    for cellj in self.chart[(x, p)]:
                        for cellk in self.chart[(m, q)]:
                            for regle in self.grammaire.getproductionshorscontextesprobabiliseesbinaires():
                                if regle.proba > 0:
                                    r = len(self.chart[(x, s)])+1
                                    self.chart[(x, s)] |= Celluleproba(
                                        lhs=regle.lhs,
                                        proba=regle.proba*cellj.proba*cellk.proba,
                                        backpointer=(m, cellj.index, cellk.index),
                                        index=r
                                    )

    def get_arbre_max(self, phrase):
        """

        :param phrase:
        :return:
        """
        axiome = self.get_axiome(phrase)
        best = max(self.chart[axiome])
        return best.get_arbre(self.chart, axiome)

    def load_grammaire(self, grammaire):
        """

        :param grammaire: grammaire hors contexte sous forme normale de Chomsky
        :type grammaire: GrammaireHorsContexteCNF
        :return: None
        """
        if not issubclass(type(grammaire), Grammairehorscontexteprobabilistecnf):
            raise TypeError('CKY ne peut fonctionner qu\'avec une grammaire hors contexte mise sous forme normale de chomsky')
        else:
            self.grammaire = grammaire

    def predit(self, phrase):
        """

        :param phrase:
        :return:
        """
        self.span = (x for x, y in enumerate(range(len(phrase)), 1))
        self.initialise(phrase)
        self.remplit(phrase)

    def est_valide(self, phrase):
        """

        :param phrase:
        :type phrase:
        :return: True si l'axiome est présent dans la case correspondante False sinon
        """
        return self.grammaire.axiome in self.chart[self.get_axiome(phrase)]

if __name__ == '__main__':
    x = CKYP()
