# coding: utf8
import codecs
from productions import *
from nonterminal import *
from terminal import *
# from ckys import *
import yaml
import pickle
import ExtracteurLexSynt
from nltk.util import ngrams


class Grammaire(object):
    def __init__(self, terminals, nonterminals, productions):
        self.__terminals = terminals
        self.__nonterminals = nonterminals
        self.__productions = productions
        # self.__axiome = [ x for x in Nonterminal.getnonterminals().keys() if str(x) == "SENT"][0]

    @property
    def nonterminals(self):
        return self.__nonterminals

    @property
    def terminals(self):
        return self.__terminals

#     @property
#     def axiome(self):
#         return self.__axiome

    @property
    def productions(self):
        return self.__productions

    def dump(self, nomdufichier, format):
        if format == "yaml":
            yaml.dump(
                data=self,
                stream=open(nomdufichier, 'w')
            )
        elif format == "pickle":
            pickle.dump(
                obj=self,
                file=open(nomdufichier, 'wb')
            )
        else:
            raise AttributeError("le paramètre format ne peut accepter 'yaml' ou 'pickle'.")

    def __repr__(self):
        return "NT = {self.nonterminals},\nT = {self.terminals},\nP = {self.productions}".format(self=self)

    def __str__(self):
        return repr(self)


class Grammairehorscontexte(Grammaire):
    def __init__(self):
        super(Grammairehorscontexte, self).__init__()
        self.__productions = Productionhorscontexte.getproductions()

    def ununarise(self, productions):
        pass

    def binarise(self, productions):
        pass


class Grammairehorscontextecnf(Grammairehorscontexte):
    def __init__(self):
        super(Grammairehorscontextecnf, self).__init__()
        self.__productions = [x for x in Productionhorscontexte.getproductions() if isinstance(x, (Productionhorscontextelexicale, Productionhorscontextebinaire))]


class Grammairehorscontexteprobabiliste(Grammaire):
    def __init__(self, terminals, nonterminals, productions):
        if not all(issubclass(type(x), Productionhorscontexteprobabilisee) for x in productions):
            raise TypeError('Attention, Les productions doivent être probabilisées')
        else:
            super(Grammairehorscontexteprobabiliste, self).__init__(terminals=terminals, nonterminals=nonterminals, productions=productions)

    def ununuarise(self, productions):
        """
            Application de l'algorithme page 195 de Roark & Sproat.

        :param productions: ensemble de sous-type de Productionhorscontexteprobabilisee
        :type productions: list(Productionhorscontexteprobabilisee)
        :return: liste de productions sans Productionhorscontexteprobabiliseeunaire et proba ajustées
        """
        symb = '{0}|{1}'
        while any(isinstance(x, Productionhorscontexteprobabiliseeunaire) for x in productions):
            for prod1 in Production.getproductions(productions, Productionhorscontexteprobabiliseeunaire):
                n_s = Nonterminal(symb.format(prod1.lhs.lhs[0], prod1.rhs.rhs[0]))
                productions.remove(prod1)
                for prod2 in Production.getproductions(productions, Productionhorscontexteprobabiliseenaire):
                    productions.remove(prod2)
                    if prod1.lhs.lhs[0] in prod2.rhs.rhs:
                        temporaire = prod2.rhs.replace(prod1.lhs.lhs[0], n_s)
                        t = type(prod2)(prod2.lhs.lhs, temporaire)
                        t.proba = prod1.proba * prod2.proba
                        productions.append(t)
                        prod2.proba *= (1 - prod1.proba)
                    productions.append(prod2)
                for prod3 in Production.getproductions(productions, Productionhorscontexteprobabilisee1):
                    productions.remove(prod3)
                    if (prod3 != prod1) and (prod3.lhs.lhs[0] == prod1.lhs.lhs[0]):
                        prod3.proba /= (1-prod1.proba)
                        productions.append(prod3)
                    elif prod3.lhs.lhs[0] == prod1.rhs.rhs[0]:
                        t = type(prod3)([n_s], prod3.rhs.rhs)
                        t.proba = prod3.proba
                        productions.append(t)
                    productions.append(prod3)
            return productions

    def markovise(self, productions, markov=1):
        """

        :param production: sous type de Production
        :param markov: integer
        :return: iterator
        """
        while any(isinstance(x, Productionhorscontexteprobabiliseenaire) for x in productions):
            for production in Production.getproductions(productions, Productionhorscontexteprobabiliseenaire):
                productions.remove(production)
                agglutine = lambda x=(1, 2, None): "".join([str(y) for y in x if x is not None])
                temp_n_s = str(production.lhs.lhs[0]) + ":"
                if markov == 0:
                    n_s = [Nonterminal(temp_n_s)]
                    binaire = Productionhorscontexteprobabiliseebinaire(
                        production.lhs.lhs,
                        [production.rhs.rhs[0], n_s]
                    )
                    binaire.proba = production.proba
                    productions.append(binaire)
                    for element in production.rhs.rhs[1:-2]:
                        productions.append(Productionhorscontexteprobabiliseebinaire(n_s, [element, n_s[0]]))
                    productions.append(Productionhorscontexteprobabiliseebinaire(n_s, production.rhs.rhs[-2:]))
                else:
                    temp = ngrams(production.rhs.rhs[:-1], markov, pad_left=True)
                    rhs = production.rhs.rhs.copy()
                    tp = Nonterminal(temp_n_s + agglutine(x=next(temp)))
                    binaire = Productionhorscontexteprobabiliseebinaire(production.lhs.lhs, [rhs.pop(0), tp])
                    binaire.proba = production.proba
                    productions.append(binaire)
                    if len(rhs) > 2:
                        for element in temp:
                            tp1 = Nonterminal(temp_n_s + agglutine(element))
                            productions.append(Productionhorscontexteprobabiliseebinaire([tp], [rhs.pop(0), tp1]))
                            tp = tp1
                    else:
                        productions.append(Productionhorscontexteprobabiliseebinaire([tp], rhs))
        return productions

    def naire2cnf(self):
        productions = self.markovise(
            self.ununuarise(
                self.productions
            ),
            markov=1
        )
        # return productions
        return Grammairehorscontexteprobabilistecnf(
            terminals=Nonterminal.getnonterminals(key=None),
            nonterminals=Terminal.getterminals(key=None),
            productions=productions
        )


class Grammairehorscontexteprobabilistecnf(Grammairehorscontexteprobabiliste):
    def __init__(self, terminals, nonterminals, productions):
        if all(
                isinstance(
                    x,
                    (
                            Productionhorscontexteprobabiliseelexicale,
                            Productionhorscontexteprobabiliseebinaire
                    )
                ) for x in productions):
            raise TypeError(''' Dans une Grammairehorscontexteprobabilistecnf,
                                les productions doivent être lexicales ou binaires.
                                '''
                            )
        else:
            super(Grammairehorscontexteprobabilistecnf, self).__init__(
                terminals=terminals,
                nonterminals=nonterminals,
                productions=productions
            )




if __name__ == '__main__':
    pass
    # with codecs.open("../corpus/sequoia-corpus+fct.id_mrg") as id_mrg:
    #     corpus = id_mrg.readlines()

    # for ligne in corpus[:10]:
    #     (nomcorpus_numero, phrase) = ligne.split('\t')
    #     (nomcorpus, numero) = nomcorpus_numero.rpartition('_')[::2]
    #     ExtracteurLexSynt.parser.parse(phrase)
    # Productionhorscontexteprobabilisee.setprobaproductions()


    # g = Grammairehorscontexteprobabiliste(
    #     terminals=Nonterminal.getnonterminals(key=None),
    #     nonterminals=Terminal.getterminals(key=None),
    #     productions=Productionhorscontexteprobabilisee.productions()
    # )
    # print(g)

    # g.dump('test1.pickle', 'pickle')
    # grammaire = pickle.load(open('test1.yaml', 'rb'))
    # cnf = grammaire.naire2cnf()
    # cnf.dump('test2.pickle', 'pickle')
    # glurps = pickle.load(open('test2.pickle', 'rb'))
    # print(glurps)
    # print()
    # print()
    # print()
    # print()
    # print(grammaire.productions)
    # print(grammaire.productions)
    # for x in grammaire.naire2cnf():
    #     print(x)
