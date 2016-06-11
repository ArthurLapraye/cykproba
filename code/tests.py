# coding: utf8
import codecs
import grammaires
import ckys
from extraire import parser
import phrases
import nonterminal, terminal, productions


def main():
    with codecs.open("corpus/sequoia-corpus+fct.id_mrg") as id_mrg:
        corpus = []
        for ligne in id_mrg:
            (nomcorpus_numero, phrase) = ligne.split('\t')
            (nomcorpus, numero) = nomcorpus_numero.rpartition('_')[::2]
            corpus.append(
                phrases.Phrase(
                    gold=phrase,
                    corpus=nomcorpus,
                    numero=numero
                )
            )

    # entrainement
    # for i in range(10):
    #     x = parser.parse(input=corpus[i].gold)
    #     corpus[i].extraction.extend(parser.parse(input=corpus[i].gold))
    # productions.Productionhorscontexteprobabilisee.setprobaproductions()

    # grammaire = grammaires.Grammairehorscontexteprobabiliste(
    #     terminals=terminal.Terminal.getterminals(),
    #     nonterminals=nonterminal.Nonterminal.getnonterminals(),
    #     productions=productions.Production.productions()
    # )
    # print(grammaire)
    # x = grammaire.ununarise(grammaire.productions)
    # print(x)


#    cky = CKY()
#    for p in corpus.splitlines():
#        gold.append(p)
#        cky.learn(p)
#    cky.dump_grammar('grammaire_sequoia')

    # test

if __name__ == '__main__':
    main()
