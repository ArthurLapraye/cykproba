# coding: utf-8

import yaml
import codecs
import sqlite3

with codecs.open("Ressources/../sequoia-corpus+fct.id_mrg") as id_mrg:
    for ligne in id_mrg:

        # nom du corpus, numero de la phrase, la phrase

        (nomcorpus_numerophrase, phrase) = ligne.split("\t")
        (nomcorpus, numerophrase) = nomcorpus_numerophrase.split('_')
        phrase = phrase[2:-2]
        print(phrase)
        break