#!/usr/bin/python3
# coding: utf8

import collections
import fractions

def get_sent_sommet(phrase):
    for x in self.grammaire['axiome']:
        try:
            sent_sommet = self.chart[(0, len(phrase))][x]
        except KeyError:
            print("La phrase n'est pas reconnue par la grammaire")
        return (sent_sommet, (0, len(phrase)))

def predit(phrase, cnf):
    print('Prédiction: ')

    chart = collections.defaultdict(lambda : collections.defaultdict(int))

    return get_sommet(remplit(phrase, cnf, initialise(phrase, cnf)), phrase)
    # return get_arbre(get_sommet(remplit(phrase, cnf, initialise(phrase, cnf, chart))))

def get_sommet(chart, phrase):
    for x in list(chart[(len(phrase), 0)]):
        if (x == "SENT") or "SENT" in x:
            print(chart[(len(phrase), 0)][x])

def get_arbre(sent_sommet):
    pattern = '({tete} {enfants})'
    tete = list(self.chart[sent_sommet[1]].keys())[0]
    if (len(sent_sommet) == 1) and (isinstance(sent_sommet, (tuple, (int, int)))):
        return pattern.format(tete=tete, enfants=tete.lower())
    else:
        if (len(sent_sommet) == 2) and (isinstance(sent_sommet, (tuple, (tuple, tuple)))):
            return pattern.format(
                tete=tete,
                enfants=" ".join([self.get_arbre(child) for child in sent_sommet[1]])
            )

def initialise(phrase, cnf):
    print('Initialisation de la charte: ')

    chart = collections.defaultdict(lambda: collections.defaultdict(int))

    (terminaux, nonterminaux, regles) = cnf

    s = 1

    for (t, _) in enumerate(phrase):
        for lhs in list(regles):
            for rhs in list(regles.get(lhs)):
                if len(rhs) == 1:
                    chart[(s, t)][lhs] = regles[lhs][rhs[0]]
                    # chart[(s, t)][lhs] = (regles[lhs][rhs[0]], ((t, s),))
    print('Chart initialisée')
    return chart


def remplit(phrase, cnf, chart):
    print('Remplissage de la charte: ')

    span = (x for (x, y) in enumerate(phrase[1:], 2))

    (terminaux, nonterminaux, regles) = cnf

    for max in span:
        for min in range(max-2, 0, -1):
            print(min, max)
            for nonterminal in nonterminaux:
                best = 0
                for rhs in regles[nonterminal]:
                    if len(rhs) == 2:
                        for mid in range(min + 1, max - 1):
                            t1 = chart[(min, mid)][rhs[0]]
                            t2 = chart[(mid, max)][rhs[1]]
                            candidate = t1 * t2 * regles[nonterminal][rhs]
                            if candidate > best:
                                best = candidate
                                # best = (candidate, ((min, mid, rhs[0]), (mid, max, rhs[1])))
                        chart[(min, max)][nonterminal] = best
    print('Chart remplie')
    return chart


def defaultdictmaker():
    return collections.defaultdict(fractions.Fraction)


def main():
    import pickle
    import evaluation
    import sys, codecs

    cnf = pickle.load(open(sys.argv[1], 'rb'))

    with codecs.open(sys.argv[2], "r") as corpus:
        for phrase in corpus:
            if not phrase.startswith('('):
                (nomcorpus_numero, phrase) = phrase.split('\t')
                (nomcorpus, numero) = nomcorpus_numero.rpartition('_')[::2]
            arbre=evaluation.readtree(evaluation.tokenize(phrase))[0]
            phrase = evaluation.getleaves(arbre)
            print("phrase_gold : ", phrase)
            print(predit(phrase, cnf))


if __name__ == '__main__':
    main()
