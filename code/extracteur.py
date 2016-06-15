#!/usr/bin/python3
# coding: utf8

import evaluation
from collections import defaultdict
import fractions
from copy import deepcopy
from collections import defaultdict
from itertools import chain,combinations

	
"""
For every unary rule
A → B, with A, B ∈ V and probability p 1  :
	1. Add a non-terminal A↓B to V .
	2. Remove A → B from P.
	3. For every production C → · A „ in P with probability p 2 , where
	·, „ ∈ V ∗
	(a) add a production to P of the form C → · A↓B „ with
	probability p 1 p 2 ;
	(b) set P(C → · A „) = (1 − p 1 ) p 2 .
	4. For every rule production in P of the form A → · with probability
	p 3 , set P(A → ·) = p 3 /(1 − p 1 ).
	5. For every rule production in P of the form B → ·,
	add productions to P of the form A↓B → · such that
	P(A↓B → ·) = P(B → ·).
"""


def CNF(terminaux,nonterminaux,regles,markov=None):
    cnf=deepcopy(regles)
    
    def binariser(nterm,prod,proba=1):
    	if prod[2:]:
    		nuNT="↓".join(prod)
    		nonterminaux.add(nuNT)
    		cnf[nterm][prod[0],nuNT]=proba
    		binariser(nuNT,prod[1:])
    	else:
    		cnf[nterm][prod]=proba
    
    for nterm in regles:
        for production in regles[nterm]:
            if production[2:]:
                binariser(nterm,production,proba=regles[nterm][production])
                del cnf[nterm][production]
    
    #Unit test : vérifier l'intégrité de la grammaire
    #Que toutes les règles sont au plus binaires
    #Que toutes les probabilités somment toujours à 1
    for nt in cnf:
    	sumproba=0
    	#print(nt)
    	for prod in cnf[nt]:
    		#print(prod)
    		if len(prod) > 2:
    			raise ValueError("Fail"+str(prod))
    		else:
    			sumproba += cnf[nt][prod]
    		
    	#print(sumproba)
    	assert(sumproba==1)
    
    regles=cnf
    cnf=deepcopy(cnf)
    
    for nterm in regles:
    	for production in regles[nterm]:
    		if not production[1:]:
    			if not production[0] in terminaux:
    				print(nterm,"=>",production)
    				singulier=production[0]
    				nouveauNT=nterm+"↑"+singulier
    				proba1=cnf[nterm][production]
    				for p in regles[singulier]:
    					cnf[nouveauNT][p]=cnf[singulier][p]
    				
    				del cnf[nterm][production]
    				for p in cnf[nterm]:
    					cnf[nterm][p]=fractions.Fraction(cnf[nterm][p],proba1)
    				
    	#print(nterm)
    
    for nt in cnf:
    	print(nt)
    	somme=sum([cnf[nt][prod] for prod in cnf[nt] ])
    	print(somme)
    	assert(somme==1)
    
    	
    		#else:
    		#	print(prod
    
    return nonterminaux, terminaux, cnf

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
    from pickle import dump as pdump
    from random import shuffle
    from sys import stdin
    from extraire import parser, sentence
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
#    argumenteur.add_argument(
#        "-y",
#        "--yaml",
#        action='store_true',
#        default=False,
#        help="Cette option permet de mettre la sortie au format YAML"
#    )
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
        help="Nom du fichier de phrases au format Phrase de sortie au format pickle."
    )

    argumenteur.add_argument(
        "-n",
        "--nb",
        type=int,
        help="chiffre servant à limiter le nombre d'éléments à prendre dans le corpus"
    )

    args = argumenteur.parse_args()

    with codecs.open(args.input, 'r', 'utf-8') as entree:
        print('Ouverture/fermeture du fichier mrg.')
        corpus = entree.read().splitlines()

    if args.shuffle:
        print('Mélange des données')
        shuffle(corpus)
    print('Traitement du corpus, consitution des règles de production.')
    
    rightside=defaultdict(lambda : defaultdict(int))
    leftside =defaultdict(int)
    
    for (i, ligne) in enumerate(corpus[:args.nb], 1):
        #print(i)
        phrase=""
        numero=None
        if not corpus[0].startswith('('):
            (nomcorpus_numero, phrase) = ligne.split('\t')
            (nomcorpus, numero) = nomcorpus_numero.rpartition('_')[::2]
            
        else:
            phrase=ligne
        
        
        arbre=evaluation.defoliate(evaluation.readtree(evaluation.tokenize(phrase))[0])
        nonterminaux,terminaux = evaluation.nodesandleaves(arbre)
        productions=evaluation.getchildren(arbre)
        
        for elem in productions:
        	leftside[elem] += len(productions[elem])
        	for prod in productions[elem]:
        		rightside[elem][prod] += 1
        
        #print(leftside)
        #print(rightside)
        
        #input()
        
        phrases.Phrase(gold=phrase,
                numero= int(numero) if numero else i,
                pos=terminaux)
        sentence = []

    if args.sentences is not None:
        print('Sortie du fichier phrases avec les phrases au format pickle')
        pdump(phrases.Phrase.phrases(), open(args.sentences, 'wb'))
    
    for nt in rightside:
        sumproba=0
        for prod in rightside[nt]:
            prodproba=fractions.Fraction(rightside[nt][prod],leftside[nt])
            rightside[nt][prod]=prodproba
            sumproba += prodproba
        assert(sumproba==1)
        
    
    grammaire=CNF(set(terminaux),set(nonterminaux),rightside)
    
    print('Fin')



if __name__ == '__main__':
    extraire_grammaire()
