
Le dossier code contient tous les scripts pour faire fonctionner le CKY.

On peut voir le dossier en trois partie:
    - l'extraction
    - PCFG
    - CKY

L'extraction (faites avec ExtracteurLexSynt.py) prend une phrase en entrée
au format mrg parenthésé, puis va générer un ensemble de productions, un ensemble de nonterminals
et un ensemble de terminals.

La PCFG ne sera que l'utilisation des trois ensembles générés par l'extracteur pour instancier une classe PCFG.
Cette classe permettra, entre autres d'accéder aux productions, nonterminals, terminals et axiome de la grammaire,
d'opérer des transformations sur elle-même mais sans jamais la modifier. Une modification instantiera une nouvelle
grammaire suivant les besoins.

CKY permet de prendre la PCFG, une phrase tokenisée, soit avec ou sans le lexique
( ["det", "n", "v"] ou ["le", "chat", "dort"]) et de prédire un arbre.
La prédiction sort la phrase au format parenthée comme en entrée.


Il faut voir les scripts handside.py, lefthandside.py et righthandside.py comme des classes abstraites.
Ce sont les classes dont productions.py hérite afin de rendre compte de tous les types de productions dont on a besoin
dans ce programme.


traitement.py permet de faire fonctionner le tout.
Il comporte plusieurs options
Exemple de ligne:
    python traitement.py mrg.txt grammaire.pickle --type_sortie pickle -G cnf -m --markov_ordre 1

Cette exemple prend en entrée un fichier au format parenthésé, et sortira une grammaire au format CNF avec
une markovisation horizontale d'ordre 1.

