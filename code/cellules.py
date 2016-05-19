# coding: utf8

class Cellule(object):
    def __init__(self, lhs, backpointer=None, index=1):
        self.lhs = lhs
        self.backpointer = backpointer
        self.index = index

    def __repr__(self):
        return "{self.lhs}, {self.backpointer}, {self.index}".format(self=self)

    def __str__(self):
        return repr(self)

    def __add__(self, other):
        return (self.lhs, other.lhs)

class Celluleproba(Cellule):
    def __init__(self, lhs, proba, backpointer, index):
        super(Celluleproba, self).__init__(lhs, backpointer, index)
        self.proba = proba

    def __repr__(self):
        return "[{self.lhs}, {self.proba}, {self.backpointer}, {self.index}]".format(self=self)

    def __str__(self):
        return repr(self)

    def __add__(self, other):
        return self.proba + other.proba

    def __mul__(self, other):
        return self.proba * other.proba

    def __sub__(self, other):
        return self.proba - other.proba

    def __truediv__(self, other):
        return self.proba / other.proba

    def __gt__(self, other):
        return self.proba > other.proba

    def get_arbre(self, charte, case=(1, 1)):
        (span, index) = case
        chaine = "({0} {1})"
        if self.backpointer is None:
            return chaine.format(self.lhs, self.lhs.lower())
        else:
            children = [(self.backpointer[0], index), (span - self.backpointer[0], index - span - 1)]
            cellules = self.backpointer[1:]

            return chaine.format(self.lhs, " ".join([self.get_arbre(charte[child[0]][child[1]][cell], child) for cell in cellules for child in children]))
