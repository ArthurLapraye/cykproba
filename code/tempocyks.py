# coding: utf8

from collections import defaultdict

class LengthError(IndexError):
    '''
        Raise a IndexError when a sequence is not right adjusted.
    '''


class Cellule(object):
    def __init__(self, nonterminal, proba, backpointer=None, index=1):
        if len(args) != 4:
            raise LengthError("Attention, Cellule reçoit nécessairement 4 arguments")
        self.lhs = nonterminal
        self.proba = proba
        self.backpointer = backpointer
        self.index = index

    def __repr__(self):
        return "[{self.lhs}, {self.proba}, {self.backpointer}, {self.index}]".format(self=self)

    def __str__(self):
        return repr(self)


class CKY(object):
    def __init__(self):
        self.chart = defaultdict(list)

    def initialise(self):
        s = next(self.span)
        for (t, mot) in enumerate(iterable=self.phrase, start=1):
            x = t-1
            for lexical in [x for x in self.grammaire if isinstance(x, ProductionHorsContexteLexicaleProbabilisee)]:
                r = len(self.chart[x][s])+1
                self.chart[x][s] |= Cellule(
                                    nonterminal=lexical.lhs,
                                    proba=lexical.proba,
                                    backpointer=None,
                                    index=r
                                )

    def remplit(self):
        for s in self.span:
            for t in range(len(self.phrase)-S+1):
                x = t-1
                for m in range(t, t+s-2):
                    p = m-x
                    q = s-p
                    for cellj in self.chart[x][p]:
                        for cellk in self.chart[m][q]:
                            for regle in [x for x in self.grammaire.productions if not isinstance(x, ProductionHorsContexteLexicaleProbabilisee)]:
                                if regle.proba > 0:
                                    r = len(self.chart[x][s])+1
                                    self.chart[][] |= Cellule(
                                        nonterminal=regle.lhs,
                                        proba=regle.proba*cellj.proba*cellk.proba,
                                        backpointer=(m, cellj.index, cellk.index),
                                        index=r
                                    )

    def get_arbre(self, cellule, coord=(1,1)):
        (span, index) = coord
        chaine = "({0} {1})"
        if cellule.backpointer is None:
            return chaine.format(cellule.lhs, cellule.lhs.lower())
        else:
            children = [(cellule.backpointer[0], index), (span-cellule.backpointer[0], index-span-1)]
            # children donne les les coordonnées des enfants, cellule.backpointer[1:] donne dans l'ordre la cellule de chaque enfant.
            cellules = cellule.backpointer[1:]

            return chaine.format(cellule.lhs, " ".join([self.get_arbre(self.chart[child[0]][child[1]][cell], child) for cell in cellules for child in children]))

    def load_grammaire(self, grammaire):
        self.grammaire = grammaire

    def load_phrase(self, phrase):
        self.phrase = phrase
        self.load_span(phrase)

    def load_span(self, phrase):
        self.span = (x for x, y in enumerate(range(len(phrase)),start=1))


class CYKmel(object):
    def __init__(self, mot=None, grammaire=None):
        """

        :param mot:
        :param grammaire:
        :return:
        """
        self.chart = {}
        self.mot = mot
        self.grammaire = grammaire
        if (mot is not None) and (grammaire is not None):
            self.initialise(mot, grammaire)
            self.fillin(mot, grammaire)

    def initialise(self, mot, grammaire):
        """
            Initialisation de la table T pour le mot u et la grammaire gr
        :param mot: mot à parser
        :param grammaire: grammaire
        :return: chart initialisée
        """
        for i in range(1, len(mot)+1):                        # On parcourt le mot à reconnaitre
            for (l, r) in grammaire:                        # On parcourt la grammaire
                if mot[i-1] == r:                           # Si lettre en cours identique à partie droite de règle
                    if (i, i+1) not in self.chart:
                        self.chart[(i, i+1)] = [(l, r)]  # On remplit la case
                    else:
                        self.chart[(i, i+1)].append((l, r))    # On rajoute une autre règle s'il y en a + qu'une
            if (i, i+1) not in self.chart:
                self.chart[(i, i+1)] = []                       # Si case vide, ajout tableau vide dedans

    def fillin(self, mot, grammaire):
        """
            Remplissage de la table T (initialisation deja  effectuee) pour le mot u et la grammaire gr
        :param mot: mot à parser
        :param grammaire: grammaire
        :return: chart
        """
        for i in range(2, len(mot)+1):                                       # On utilise y et i pour parcourir la chart
            for y in range(1, (len(mot)-i+2)):
                for j in range(y+1, i+y):                                    # La variable j est utilisée pour trouver la moitié du protomot
                    for (a, b) in self.chart[(y, j)]:                        # On regarde dans paires de cases nécéssaire pour remplir la prochaine
                        for (c, d) in self.chart[(j, i+y)]:
                            for (l, r) in grammaire:                         # On parcourt la grammaire
                                if r == a+c:                                 # S'il y a une règle dans la grammaire qui a en partie droite la concaténation des parties gauches des règles présentes dans les paires de cases
                                    if (y, i+y) not in self.chart:
                                        self.chart[(y, i+y)] = [(l, r)]      # On remplit la case
                                    else:
                                        self.chart[(y, i+y)].append((l, r))  # ajout de la règle si elle n'existe pas
                    if (y, i+y) not in self.chart:
                        self.chart[(y, i+y)] = []

    def is_valid(self, mot):
        """
            Fonction booléenne qui regarde si l'axiome se trouve dans la case la plus haute du tableau.
        :param mot: mot à parser
        :return: True/False
        """
        if "S" in self.chart[(1, len(mot)+1)]:
            return True
        return False

    def get_arbre(self, best=True, nbest=1):
        """
            Cette fonction suivant les options passées, va retourner un arbre ou plusieurs.

        :param best: renvoie le meilleur arbre
        :param nbest: renvoie les n-meilleurs arbres
        :return: arbre ou liste d'arbres
        """
        pass

    def __repr__(self):
        """
            La fonction de représentation affichera l'arbre (ou la foret) avec en entête la grammaire et le mot à parser

            str(mot), str(grammaire), str(self)

        :return: "\n".join([str(mot), str(grammaire), str(self)])
        """
        return

    def __str__(self):
        return repr(self)


class CYKP(CYK):
    """
        CYK probabiliste:
            apllication d'un argmax sur les cellules du tableau
            application d'un k-possibilites sur les cellules du tableau
    """
    def initialise(self):
        s = next(self.span)
        for t, mot in enumerate(iterable=self.phrase):
            x = t-1
            for lexical in [x for x in self.grammaire if isinstance(x, ProductionHorsContexteLexicaleProbabilisee)]:
                pass

    def fillin(self, mot, grammaire):
        pass






def main():
    print("En cours d'execution")

if __name__ == '__main__':
    main()