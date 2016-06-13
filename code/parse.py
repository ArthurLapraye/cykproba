# coding: utf8
import argparse


def parse():
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
    parse()
