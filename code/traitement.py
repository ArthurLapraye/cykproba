#!/usr/bin/python
# coding: utf8
import codecs
import grammaires
import ExtracteurLexSynt
import nonterminal
import terminal
import productions


def main():
    with codecs.open("../corpus/sequoia-corpus+fct.id_mrg") as id_mrg:
        corpus = id_mrg.readlines()

    for ligne in corpus[:10]:
        (nomcorpus_numero, phrase) = ligne.split('\t')
        (nomcorpus, numero) = nomcorpus_numero.rpartition('_')[::2]
        ExtracteurLexSynt.parser.parse(phrase)
    productions.Productionhorscontexteprobabilisee.setprobaproductions()


    g = grammaires.Grammairehorscontexteprobabiliste(
        terminals=nonterminal.Nonterminal.getnonterminals(key=None),
        nonterminals=terminal.Terminal.getterminals(key=None),
        productions=productions.Productionhorscontexteprobabilisee.productions()
    )
    print(g)


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
