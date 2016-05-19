# coding: utf-8

# import yaml
# import codecs
# import sqlite3
# from Extracteur import *
from grammaire import *




#with codecs.open("Ressources/../sequoia-corpus+fct.id_mrg") as id_mrg:
#    id_mrg.readlines()
#    cero = [1,2,3,4,5]
#    for x in range(len(cero)):
#        print('train {0}, test {1}'.format(cero[:x]))


# prendre un ensemble de sequences
#     extraire grammaire
#     cky(e E sequences, grammaire extraite): ensemble de sequences
# retourne corpus aligné (gold, prediction)

def extraire(corpus, parseur, typesortie):
    if issubclass(typesortie, Grammaire):
        for p in corpus:
            parseur.parse(p)
        return typesortie(Nonterminal.nonterminals, Terminals.terminals, Production.productions)

def main():
    # lecture corpus
    (train, test) = [0, 0] # ligne ou faudra ouvrir les phrases
    # lecteur de phrases parenthésées
    parseur = ""
    grammaire = extraire(corpus=corpus, parseur, typesortie=Grammairehorscontexteprobabilisee)

    grammaire.dump('grammairehorscontexteprobabilisee.pickle')
    grammaire.dump('grammairehorscontexteprobabilisee.yaml')

    # conversion vers une grammaire CNF
    gcnf = grammaire.verscnf()

    gcnf.dump('grammairehorscontextecnfprobabilisee.pickle')
    gcnf.dump('grammairehorscontextecnfprobabilisee.yaml')

    # instanciation du cky, chargement de la grammaire
    cky = CKY()
    cky.load(gcnf)

    for gold in test:
        pred = cky.predit(p)
    # dumper la sortie (gold, pred) dans un fichier texte


def fonction(sequence):
    for x in range(len(sequence)):
        yield sequence[:x]+sequence[x+1:], sequence[x]

train_test = lambda sequence: ((sequence[:x]+sequence[x+1:],sequence[x]) for x in range(len(sequence)))

decoupe = lambda line, n: [line[i:i+n] for i in range(0, len(line), n)]


def n_fold(sequence):
    pass

# segmenter corpus train test
#
#
#