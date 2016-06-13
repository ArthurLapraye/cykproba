#!/usr/bin/python3
# coding: utf8

import grammaires
import productions
import nonterminal
from yaml.representer import Representer
import yaml



class CKY_TITOV(object):
    def __init__(self):
        self.chart = dict()

    def get_sent_sommet(self, phrase):
        for x in self.grammaire['axiome']:
            try:
                sent_sommet = self.chart[(0, len(phrase))][x]
            except KeyError:
                print("La phrase n'est pas reconnue par la grammaire")
            return (sent_sommet, (0, len(phrase)))

    def load_grammar(self, grammaire):
        print("Chargement de la grammaire: \n")
        if not issubclass(type(grammaire), grammaires.Grammairehorscontexteprobabilistecnf):
            raise TypeError('CKY ne peut fonctionner qu\'avec une grammaire hors contexte mise sous forme normale de chomsky')
        else:
            self.grammaire = grammaire

    def predit(self, phrase):
        print('Prédiction: ')
        self.span = (x for x,y in enumerate(phrase, 1))
        self.initialise(phrase)
        self.remplit(phrase)

        return self.get_arbre(self.get_sent_sommet(phrase))

    def initialise(self, phrase):
        print('Initialisation de la charte: ')
        s = next(self.span)
        for (t, mot) in enumerate(phrase):
            self.chart[(s, t)] = {}
            for terminal in self.grammaire.terminals:
                self.chart[(s, t)][terminal] = 0
                for lexicale in productions.Production.subset_productions(self.grammaire.productions, productions.Productionhorscontexte1lexicaleprobabilisee, terminal):
                    self.chart[(s, t)][terminal] = (lexicale.proba, ((t, s)))

    def remplit(self, phrase):
        print('Remplissage de la charte: ')
        for max in self.span:
            for min in range(max-2, 0, -1):
                self.chart[(min, max)] = dict()
                for nonterminal in self.grammaire["nonterminals"]:
                    best = 0
                    self.chart[(min, max)][nonterminal] = (0,)
                    for binaire in productions.Production.subset_productions(
                            self.grammaire.productions,
                            productions.Productionhorscontexte2binaireprobabilisee, nonterminal):
                        for mid in range(min + 1, max - 1):
                            t1 = self.chart[(min, mid)][binaire[1][0]]
                            t2 = self.chart[(mid, max)][binaire[1][1]]
                            if (t1[0] == 0) or (t2[0] == 0):
                                candidate = 0
                            else:
                                candidate = t1[0] * t2[0] * binaire.proba
                            if candidate > best:
                                best = (candidate, ((min, mid, binaire[1][0]), (mid, max, binaire[1][1])))
                    self.chart[(min, max)][nonterminal] = best

    def get_arbre(self, sent_sommet):
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

def main2():
    import pickle
    from nonterminal import nonterminal_representer

    yaml.add_representer(InfiniteDict, Representer.represent_dict)
    yaml.add_representer(nonterminal.Nonterminal, nonterminal_representer)

    cky = CKY_TITOV()
    grammaire = pickle.load(open("grammaire_200_pcnf.pickle", 'rb'))
    cky.load_grammar(grammaire=grammaire)
    b = "Cet été".split(' ')
    # for p in grammaire.productions:
    #     print(p)
    print(cky.predit(b))


def main():
    import argparse
    import pickle

    argumenteur = argparse.ArgumentParser(
        prog="parse.py",
        description="""
            Programmae prenant une chaine de caratère et à partir d'une gammaire, prédit la structure la plus probable.
            Ce parseur peut prédire ou bien simplement reconnaitre si la chaine donnée en param§tre est reconnue par
            la grammaire.
            """,

    )

    group1 = argumenteur.add_argument_group(
        title="debug-mode",
        description="permet de parser une phrase et de sortir la prédiction à l'écran. --debug mode --"
    )

    group2 = argumenteur.add_argument_group(
        title="mode Parsing intégral",
        description="prend un fichier de phrases et sort les résultats des prédictions dans un fichier de sortie."
    )

    group1.add_argument(
        "-i",
        "--input",
        type=str,
        help="""
            -i permet de passer une phrase en ligne de commande au parseur
            et d'afficher le résultat de la prédiction à l'écran
        """
    )

    group2.add_argument(
        "-f",
        "--fileinput",
        help="-f permet de passer un fichier texte au parseur"
    )

    group2.add_argument(
        "-o",
        "--output",
        default=False,
        help="-o permet de sortir le résultat du parsing dans un fichier texte"
    )

    argumenteur.add_argument(
        "-g",
        "--load-grammaire",
        required=True,
        help="""
            Pour fonctionner, un parseur doit avoir une grammaire en mémoire
            afin de vérifier si la/les phrase(s) passées sont reconnues par la grammaire
        """
    )

    args = argumenteur.parse_args()
    if args.fileinput is not None:
        if args.fileinput.endswith('.ph.txt'):
            with open(args.fileinput, 'rb') as file:
                phrases = pickle.load(file)
        else:
            with open(args.fileinput, 'r') as file:
                phrases = [x.split(' ') for x in file.readlines()]

    if args.input:
        grammaire = pickle.load(open(args.load_grammaire, "rb"))
        cky = CKY_TITOV()
        cky.load_grammar(grammaire)
        print(str(args.input.split(' ')))
        print(cky.predit(args.input.split(' ')))

    elif args.fileinput:
        cky = CKY_TITOV()
        cky.load_grammar(args.load_grammaire)
        if isinstance(phrases[0], phrases.Phrase):
            for phrase in phrases:
                phrase.predit = cky.predit(phrase.pos_gold)
        else:
            temp = []
            for phrase in phrases:
                temp.append([phrase, cky.predit(phrase)])
            tmp = iter([".gold.", ".pred."])
            for phrass in zip(temp):
                nomfichier = args.output.rpartition('.')[::2]
                nomfichier.insert(1, next(tmp))
                with open(nomfichier, "w") as sortie:
                    for p in phrass:
                        sortie.write(p+"\n")


if __name__ == '__main__':
    main()
