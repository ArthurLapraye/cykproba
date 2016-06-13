# coding: utf8
import productions
import terminal
import nonterminal
import yaml
import pickle
from nltk.util import ngrams
import collections
import lefthandside
import righthandside
import errors


class Grammaire(collections.Mapping):

    def __init__(self, **kwargs):
        self.__dico = kwargs
        self.__setaxiome()
        self.check_length(4, kwargs, "==")
        self.check_type(kwargs["productions"], productions.Production)

    def check_type(self, iterable, *types):
        if not all(isinstance(x, types) for x in iterable):
            raise TypeError(
                "Toutes les prpductions d'une {name} doivent être des sous types de {types}".format(
                    name=self.__class__.__name__,
                    types=" et/ou ".join([x.__name__ for x in types])
                )
            )

    def check_length(self, i, iterable, equation="=="):
        if equation == "==":
            if not (len(iterable) == i):
                raise errors.LengthError(
                    'Une {name} doit faire {equation} {i} élément(s)'.format(
                        name=self.__class__.__name__, i=i, equation=equation
                    )
                )
        elif equation == "<=":
            if not (len(iterable) <= i):
                raise errors.LengthError(
                    'Une {name} doit faire {equation} {i} élément(s)'.format(
                        name=self.__class__.__name__, i=i, equation=equation
                    )
                )
        elif equation == ">=":
            if not (len(iterable) >= i):
                raise errors.LengthError(
                    'Une {name} doit faire {equation} {i} élément(s)'.format(
                        name=self.__class__.__name__, i=i, equation=equation
                    )
                )
        elif equation == "!=":
            if not (len(iterable) != i):
                raise errors.LengthError(
                    'Une {name} doit faire {i} {equation} élément(s)'.format(
                        name=self.__class__.__name__, i=i, equation=equation
                    )
                )
        elif equation == ">":
            if not (len(iterable) > i):
                raise errors.LengthError(
                    'Une {name} doit faire {i} {equation} élément(s)'.format(
                        name=self.__class__.__name__, i=i, equation=equation
                    )
                )
        elif equation == "<":
            if not (len(iterable) < i):
                raise errors.LengthError(
                    'Une {name} doit faire {i} {equation} élément(s)'.format(
                        name=self.__class__.__name__, i=i, equation=equation
                    )
                )

    def __setaxiome(self):
        lhss = {x[0][0] for x in self['productions']}
        rhss = set()
        for x in self['productions']:
            rhss |= set([f for f in x[1] if isinstance(f, nonterminal.Nonterminal)])
        self.__dico["axiome"] = lhss - rhss

    def dump(self, nomdufichier, extention):
        if extention == "yaml":
            yaml.dump(
                data=self,
                stream=open(nomdufichier, 'w')
            )
        elif extention == "pickle":
            pickle.dump(
                obj=self,
                file=open(nomdufichier, 'wb')
            )
        else:
            raise AttributeError("le paramètre format ne peut accepter 'yaml' ou 'pickle'.")

    def __getitem__(self, item): return self.__dico[item]

    def __iter__(self): return iter(self.__dico)

    def __len__(self): return len(self.__dico)

    def __repr__(self):
        return "NT = {nonterminals},\nT = {terminals},\nS = {axiome},\nP = {productions}".format(
            nonterminals=self["nonterminals"],
            terminals=self["terminals"],
            axiome=self["axiome"],
            productions=self["productions"]
        )

    def __str__(self): return repr(self)


class Grammairehorscontexte(Grammaire):
    def __init__(self, **kwargs):
        super(Grammairehorscontexte, self).__init__(**kwargs)
        self.check_type(
            kwargs['productions'],
            productions.Productionhorscontexte
        )

    def ununarise(self, productions):
        pass

    def binarise(self, productions):
        pass


class Grammairehorscontextecnf(Grammairehorscontexte):
    def __init__(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        super(Grammairehorscontextecnf, self).__init__(**kwargs)
        self.check_type(
            kwargs['productions'],
            productions.Productionhorscontexte2binaire,
            productions.Productionhorscontexte1lexicale
        )


class Grammairehorscontexteprobabiliste(Grammaire):
    """

    """
    def __init__(self, **kwargs):
        """

        :param kwargs:
        :type kwargs:
        :return:
        """
        super(Grammairehorscontexteprobabiliste, self).__init__(**kwargs)
        self.check_type(
            kwargs['productions'],
            productions.Productionhorscontexteprobabilisee,
            productions.Productionhorscontexte1probabilisee,
            productions.Productionhorscontexte2binaireprobabilisee,
            productions.Productionhorscontexte1lexicaleprobabilisee,
            productions.Productionhorscontexte1unaireprobabilisee,
            productions.ProductionhorscontexteNaireprobabilisee
        )

    def ununuarise(self, prods):
        """
            Application de l'algorithme page 195 de Roark & Sproat.

        :param productions: ensemble de sous-type de Productionhorscontexteprobabilisee
        :type productions: list(Productionhorscontexteprobabilisee)
        :return: liste de productions sans Productionhorscontexteprobabiliseeunaire et proba ajustées
        """
        symb = '{0}|{1}'
        te = []
        print('Ununarise')
        while any(isinstance(x, productions.Productionhorscontexte1unaireprobabilisee) for x in prods):
            print('Ununirasion en cours...')
            for prod1 in productions.Production.subset_productions(prods, productions.Productionhorscontexte1unaireprobabilisee):
                x = productions.Production.subset_productions(prods, productions.ProductionhorscontexteNaireprobabilisee)
                y = productions.Production.subset_productions(prods, productions.Productionhorscontexte1probabilisee)
                print("Boucle 1")
                n_s = nonterminal.Nonterminal(symb.format(prod1[0][0], prod1[1][0]))
                prods.remove(prod1)
                for prod2 in x:
                    print('boucle 2')
                    if prod1[0][0] in prod2[1]:
                        temporaire = prod2[1].replace(types=righthandside.RighthandsideNaire, old=prod1[0][0], new=n_s)
                        t = type(prod2)(prod2[0], temporaire)
                        t.proba = prod1.proba * prod2.proba
                        prods.append(t)
                        prod2.proba *= (1 - prod1.proba)
                    prods.append(prod2)
                for prod3 in y:
                    print('Boucle 3')
                    if (prod3 != prod1) and (prod3[0][0] == prod1[0][0]):
                        prod3.proba /= (1-prod1.proba)
                        prods.append(prod3)
                    elif prod3[0][0] == prod1[1][0]:
                        t = type(prod3)(lefthandside.Lefthandsidehorscontexte(n_s), prod3[1])
                        t.proba = prod3.proba
                        prods.append(t)
                    prods.append(prod3)
            print('fin de boucle')
        return prods

    def markovise(self, prods, markov=1):
        """

        :param prods: sous type de Production
        :param markov: integer
        :return: iterator
        """
        print('markovise')
        while any(isinstance(x, productions.ProductionhorscontexteNaireprobabilisee) for x in prods):
            print('Markovisation en cours...')
            for production in productions.Production.subset_productions(
                    prods, productions.ProductionhorscontexteNaireprobabilisee):
                prods.remove(production)
                agglutine = lambda x=(1, 2, None): "".join([str(y) for y in x if x is not None])
                temp_n_s = str(production[0][0]) + ":"
                if markov == 0:
                    n_s = nonterminal.Nonterminal(temp_n_s)
                    binaire = productions.Productionhorscontexte2binaireprobabilisee(
                        production[0],
                        righthandside.Righthandside2binaire(production[1][0], n_s)
                    )
                    binaire.proba = production.proba
                    prods.append(binaire)
                    for element in production[1][1:-2]:
                        prods.append(
                            productions.Productionhorscontexte2binaireprobabilisee(
                                lefthandside.Lefthandsidehorscontexte(n_s),
                                righthandside.Righthandside2binaire(element, n_s[0])
                            )
                        )
                    prods.append(
                        productions.Productionhorscontexte2binaireprobabilisee(
                            lefthandside.Lefthandsidehorscontexte(n_s),
                            righthandside.Righthandside2binaire(production[1][-2:])
                        )
                    )
                else:
                    temp = ngrams(production[1][:-1], markov, pad_left=True)
                    rhs = production[1]
                    tp = nonterminal.Nonterminal(temp_n_s + agglutine(x=next(temp)))
                    binaire = productions.Productionhorscontexte2binaireprobabilisee(
                        production[0],
                        righthandside.Righthandside2binaire(rhs.list[0], tp)
                    )
                    binaire.proba = production.proba
                    prods.append(binaire)
                    if len(rhs) > 2:
                        for element in temp:
                            tp1 = nonterminal.Nonterminal(temp_n_s + agglutine(element))
                            prods.append(
                                productions.Productionhorscontexte2binaireprobabilisee(
                                    lefthandside.Lefthandsidehorscontexte(tp),
                                    righthandside.Righthandside2binaire(rhs.list[0], tp1)
                                )
                            )
                            tp = tp1
                    else:
                        prods.append(
                            productions.Productionhorscontexte2binaireprobabilisee(
                                lefthandside.Lefthandsidehorscontexte(tp),
                                righthandside.Righthandside2binaire(rhs)
                            )
                        )
        return prods

    def naire2cnf(self, markov=100):
        """

        :param markov:
        :return:
        """
        print("Binarisation")
        return Grammairehorscontexteprobabilistecnf(
            terminals=nonterminal.Nonterminal.nonterminals(),
            nonterminals=terminal.Terminal.terminals(),
            productions=self.markovise(self.ununuarise(list(self['productions'])),markov=markov)
        )


class Grammairehorscontexteprobabilistecnf(Grammairehorscontexteprobabiliste):
    """

    """
    def __init__(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        self.check_type(
            kwargs['productions'],
            productions.Productionhorscontexte1lexicaleprobabilisee,
            productions.Productionhorscontexte2binaireprobabilisee
        )
        super(Grammairehorscontexteprobabilistecnf, self).__init__(**kwargs)


if __name__ == '__main__':
    pass
