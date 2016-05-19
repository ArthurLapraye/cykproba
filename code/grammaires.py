# coding: utf8
from productions import *
from nonterminal import *
from terminal import *
# from ckys import *
import yaml
import pickle


class Grammaire(object):
    def __init__(self, terminals, nonterminals, productions):
        self.__terminals = terminals
        self.__nonterminals = nonterminals
        self.__productions = productions
        self.__axiome = [ x for x in Nonterminal.getnonterminals().keys() if str(x) == "SENT"][0]

    @property
    def nonterminals(self):
        return self.__nonterminals

    @property
    def terminals(self):
        return self.__terminals

    @property
    def axiome(self):
        return self.__axiome

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
        return "NT = {self.nonterminals},\nT = {self.terminals},\nS = {self.axiome},\nP = {self.productions}".format(self=self)

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

    def ununarise(self, productions):
        symb = '{0}|{1}'
        for prod1 in Production.getproductions(productions, Productionhorscontexteprobabiliseeunaire):
            n_s = Nonterminal(symb.format(prod1.lhs.lhs[0], prod1.rhs.rhs[0]))
            productions.remove(prod1)
            for prod2 in Production.getproductions(productions, Productionhorscontexteprobabiliseenaire):
                if prod1.lhs.lhs[0] in prod2.rhs.rhs:
                    temporaire = prod2.rhs.replace(prod1.lhs.lhs[0], n_s)
                    t = type(prod2)(prod2.lhs.lhs, temporaire)
                    t.proba = prod1.proba * prod2.proba
                    productions.append(t)
                    prod2.proba = (1 - prod1.proba) * prod2.proba
            for prod3 in Production.getproductions(productions, Productionhorscontexteprobabilisee1):
                if (prod3 != prod1) and (prod3.lhs.lhs[0] == prod1.lhs.lhs[0]):
                    prod3.proba = prod3.proba / (1-prod1.proba)
                elif prod3.lhs.lhs[0] == prod1.rhs.rhs[0]:
                    t = type(prod3)([n_s], prod3.rhs.rhs)
                    t.proba = prod3.proba
                    productions.append(t)
        return productions

    def binarise(self, productions):
        symb = lambda x, y: "{x}:{y}".format(x=str(x), y="-".join([str(e) for e in y]))
        if any(isinstance(x, Productionhorscontexteprobabiliseeunaire) for x in productions):
            raise Warning('Attention il reste des productions unaires dans votre ensemble de productions')
        else:
            while not all(isinstance(x, (Productionhorscontexteprobabiliseebinaire, Productionhorscontexteprobabiliseelexicale)) for x in productions):
                for prod1 in Production.getproductions(productions, Productionhorscontexteprobabiliseenaire):
                    if len(prod1.rhs.rhs) == 2:
                        productions.remove(prod1)
                        x = Productionhorscontexteprobabiliseebinaire(prod1.lhs.lhs, prod1.rhs.rhs)
                        x.proba = prod1.proba
                        productions.append(x)
                    else:
                        new_symb = Nonterminal("{0}:{1}".format(prod1.lhs.lhs[0], "".join([str(x) for x in prod1.rhs.rhs[:-1]])))
                        print(new_symb)
                        n_s = Nonterminal(symb(prod1.lhs.lhs[0], prod1.rhs.rhs[:-1]))
                        productions.remove(prod1)
                        temp = Productionhorscontexteprobabiliseebinaire(prod1.lhs.lhs, [n_s, prod1.rhs.rhs[-1]])
                        temp.proba = prod1.proba
                        productions.append(temp)
                        productions.append(Productionhorscontexteprobabiliseenaire([n_s], prod1.rhs.rhs[:-1]))
            for x in productions:
                print(x)
#            nary = productions.getproductions()[0]
#            while productions.getproductions() != []:
#                new_symb = Nonterminal("{0}:{1}".format(nary.getlhs[0], "".join(nary.rhs[:-1])))
#                nary = productions.pop(nary)
#                x = Productionhorscontexteprobabiliseebinaire(nary.getlhs, (new_symb, nary.rhs[-1]))
#                x.proba = nary.proba
#                productions.append(Productionhorscontexteprobabiliseebinaire((new_symb,), (nary.rhs[:-1],)))
#            return productions

    def markovise(self, n=0):
        pass

    def naire2cnf(self):
        productions = self.binarise(self.ununarise(self.productions))

        return Grammairehorscontexteprobabilistecnf()


class Grammairehorscontexteprobabilistecnf(Grammairehorscontexteprobabiliste):
    def __init__(self):
        if all(
                isinstance(
                    x,
                    (
                            Productionhorscontexteprobabiliseelexicale,
                            Productionhorscontexteprobabiliseebinaire
                    )
                ) for x in Productionhorscontexteprobabilisee.getproductions()):
            raise TypeError(''' Dans une Grammairehorscontexteprobabilistecnf,
                                les productions doivent être lexicales ou binaires.
                                '''
                            )
        else:
            super(Grammairehorscontexteprobabilistecnf, self).__init__()




if __name__ == '__main__':
    # Productionhorscontexteprobabiliseeunaire([Nonterminal("SENT")], [Nonterminal("VN")])
    # Productionhorscontexteprobabiliseelexicale([Nonterminal("VN")], [Terminal('v')])
    # Productionhorscontexteprobabiliseebinaire([Nonterminal("VP")], [Nonterminal('V'), Nonterminal('NP')])
    # Productionhorscontexteprobabiliseelexicale([Nonterminal("V")], [Terminal('v')])
    # Productionhorscontexteprobabiliseebinaire([Nonterminal("NP")], [Nonterminal("Det"), Nonterminal("N")])
    # Productionhorscontexteprobabiliseenaire([Nonterminal("NP")], [Nonterminal('Det'), Nonterminal('N'), Nonterminal('ADJ'), Nonterminal('vert'), Nonterminal('Q')])
    # Productionhorscontexteprobabilisee.setprobaproductions()
    # g = Grammairehorscontexteprobabiliste(
    #     terminals=Nonterminal.getnonterminals(key=None),
    #     nonterminals=Terminal.getterminals(key=None),
    #     productions=Productionhorscontexteprobabilisee.productions()
    # )

    # g.dump('test1.yaml', 'pickle')
    grammaire = pickle.load(open('test1.yaml', 'rb'))
    print(grammaire.productions)
    # print(grammaire.productions)
    grammaire.naire2cnf()

    #for prod in grammaire.productions:
    #    print(prod.__dict__)
    #    print(prod.getproductions())