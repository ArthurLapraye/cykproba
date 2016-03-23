# coding: utf-8

def CKY(iterable, grammaire):
    """

        Pour i = 1 à |m|
             P[i, i]  := ensemble des non-terminaux  N tel que  N \rightarrow m[i] est une règle de la grammaire
        Pour d = 1 à |m|-1
            Pour i = 1 à |m|-d
                 j := i+d
                  P[i, j]  := ensemble vide
                 Pour tout k = i à j-1
                          Pour tout  B est dans   P[i, k] et  C est dans P[k+1, j]
                                    Pour tout non-terminal  N tel que  N \rightarrow BC est une règle
                                          Ajouter  N à P[i, j]
        Retourne oui si S  est dans P[1, |m|]  ; non sinon.

    :param iterable: objet sur lequel on peut appliquer une opération itérative
    :param grammaire: un objet de type Grammaire
    :return: tableau
    """
    P = {}
    for i in len(iterable):
        for (gauche, droite) in grammaire.P.items():
            if droite == iterable[i]:
                P[(i, i)] =
