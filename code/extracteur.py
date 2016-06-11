# coding: utf8


def extraire_grammaire():
    """
        Cette fonction met en place un système d'arguments/options.
        On peut soit extraire une grammaire à partir d'un fichier d'entrée ou bien
        transformer des phrases au format parenthésé en liste de postag.
    :return: None
    """
    import argparse
    import nonterminal
    import terminal
    import productions
    import grammaires
    import codecs
    from yaml import dump as ydump
    from pickle import dump as pdump
    from random import shuffle
    from sys import stdin
    from extraire import parser
    import phrases

    global sentence

    argumenteur = argparse.ArgumentParser(
        prog="extracteur.py",
        description="""
            Ce programme sert à prendre un fichier au format parenthésé,
            puis d'en extraire une grammaire au format que vous voulez,
            dans la limite des choix proposés en options.
        """
    )

    argumenteur.add_argument(
        "input",
        default=stdin,
        metavar="MRG",
        help="""
            input doit être une chaine de caractères
            représentant le nomdu fichier s'entrée.
        """
    )
    argumenteur.add_argument(
        "output",
        metavar="GRAMMAIRE",
        help="""
            output doit être une chaine de caractères
            qui représentera le nom du fichier de sortie.
        """
    )
    argumenteur.add_argument(
        "-y",
        "--yaml",
        action='store_true',
        default=False,
        help="Cette option permet de mettre la sortie au format YAML"
    )
    argumenteur.add_argument(
        "-p",
        "--pickle",
        action='store_true',
        default=False,
        help="Cette option permet de mettre a sortie au format PICKLE"
    )
    argumenteur.add_argument(
        "-F",
        "--cfg",
        default=False,
        action="store_true",
        help="La grammaire extraite sera hors contexte"
    )
    argumenteur.add_argument(
        "-C",
        "--cnf",
        default=False,
        action="store_true",
        help="La grammaire extraite sera en forme normale de Chomsky"
    )
    argumenteur.add_argument(
        "-P",
        "--pcfg",
        default=False,
        action="store_true",
        help="La grammaire extraite sera probabilisée"
    )
    argumenteur.add_argument(
        "-N",
        "--pcnf",
        default=False,
        action="store_true",
        help="""
            La grammaire extraite sera sous forme
            normale de Chomsky et probabilisée
        """
    )
    argumenteur.add_argument(
        "-M",
        "--markov",
        default=100,
        const=1,
        nargs="?",
        type=int,
        help="""Option permettant de modifier la binarisation
             en rajoutant du contexte, par défaut, la markovisation
             sera d'ordre infini, en mettant juste -M ou --markov
             elle sera d'ordre 1, sinon elle sera de l'ordre que vous souhaitez."""
    )
    argumenteur.add_argument(
        "-S",
        "--shuffle",
        default=False,
        action="store_true",
        help="Option qui permet de mélanger l'input"
    )

    argumenteur.add_argument(
        "-Y",
        "--sentences",
        default=False,
        action='store_true',
        help="sort dans un fichier yaml les objets Phrase composant le corpus."
    )

    argumenteur.add_argument(
        "-n",
        "--nb",
        type=int,
        help="chiffre servant à limiter le nombre d'éléments à prendre dans le corpus"
    )

    args = argumenteur.parse_args()

    with codecs.open(args.input, 'r', 'utf-8') as entree:
        corpus = entree.read().splitlines()

    if args.shuffle:
        shuffle(corpus)

    for (i, ligne) in enumerate(corpus[:args.nb], 1):
        if not corpus[0].startswith('('):
            (nomcorpus_numero, phrase) = ligne.split('\t')
            (nomcorpus, numero) = nomcorpus_numero.rpartition('_')[::2]
            parser.parse(phrase)
            phrases.Phrase(
                gold=phrase,
                corpus=nomcorpus,
                numero=int(numero),
                pos=sentence
            )
        else:
            parser.parse(ligne)
            phrases.Phrase(
                gold=ligne,
                pos=sentence
            )
        sentence = []

    if args.sentences:
        pdump(phrases.Phrase.phrases(), open("sortie3.pickle", 'wb'))

    productions.Production.setprobaproductions()

    tmp = grammaires.Grammairehorscontexteprobabiliste(
        terminals=terminal.Terminal.terminals(),
        nonterminals=nonterminal.Nonterminal.nonterminals(),
        productions=productions.Production.productions()
    )

    if args.pickle:
        if args.pcfg:
            with open(args.output+"_"+"pcfg"+".pickle", "wb") as f:
                pdump(tmp, f)
        if args.cfg:
            # ajouter Grammairehorscontexte(tmp) cast de tmp
            # soit passage de Productionhorscontexteprobabilisee à Productionhorscontexte
            with open(args.output+"_"+"cfg"+".pickle", 'wb') as f:
                pdump(tmp, f)
        cnf = tmp.naire2cnf(markov=args.markov)
        if args.pcnf:
            with open(args.output+"_"+"pcnf"+".pickle", "wb") as f:
                pdump(cnf, f)
        if args.cnf:
            # Grammairehorscontextecnf(cnf)
            with open(args.output+"_"+"cnf"+".pickle", "wb") as f:
                pdump(cnf, f)
    # remettre à zéro tous les compteurs
    if args.yaml:
        if args.pcfg:
            with codecs.open(args.output+"_"+"pcfg"+".yaml", "w", "utf8") as f:
                ydump(tmp, f)
        if args.cfg:
            # ajouter Grammairehorscontexte(tmp) cast de tmp
            # soit passage de Productionhorscontexteprobabilisee à Productionhorscontexte
            with codecs.open(args.output+"_"+"cfg"+".yaml", 'w', 'utf8') as f:
                ydump(tmp, f)
        cnf = tmp.naire2cnf(markov=args.markov)
        if args.pcnf:
            with codecs.open(args.output+"_"+"pcnf"+".yaml", "w", 'utf8') as f:
                ydump(cnf, f)
        if args.cnf:
            # Grammairehorscontextecnf(cnf)
            with codecs.open(args.output+"_"+"cnf"+".yaml", "w", "utf8") as f:
                ydump(cnf, f)


if __name__ == '__main__':
    extraire_grammaire()
