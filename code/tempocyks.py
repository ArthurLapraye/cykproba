# coding: utf8


class CYK(object):
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
    def initialise(self, mot, grammaire):
        pass

    def fillin(self, mot, grammaire):
        pass
