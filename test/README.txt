Ce dossier de test contient des exemples de sorties des scripts du projet CYK probabiliste.

Les fichiers train.mrg et test.mrg ont été obtenus 
à partir du fichier sequoia-corpus+fct.mrg_strict, avec le script dispatch.py.
Ils représentent respectivement un corpus d'entraînement et un corpus de test.

Le fichier grammairetraining.pickle a été créé à partir de train.mrg avec le script
extracteur.py, puis a été complété en rajoutant les règles de production lexicales 
d'une grammaire obtenue à partir du fichier sequoia-corpus+fct.mrg_strict complet.

Le fichier sortietest.mrg représente le résultat de l'analyse des phrases de test.mrg
par le script ckys.py avec la grammaire grammairetraining.pickle

Enfin, le fichier evaluation.txt donne le résultat de l'évaluation de sortietest.mrg
en comparant au gold de test.mrg.
