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
	
	for nt in regles:
		for prod in regles[nt]:
			if not prod[1:]:
				if nt == prod[0]:
					raise ValueError("Autorécriture",nt)
			
	def binariser(nterm,prod,proba=1):
		if prod[2:]:
			nuNT="↓".join(prod[1:])
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
		for prod in cnf[nt]:
			if len(prod) > 2:
				raise ValueError("Fail : "+prod)
			else:
				sumproba += cnf[nt][prod]
		assert(sumproba==1)
	
	regles=cnf
	cnf=deepcopy(cnf)
	modified=True
	i=0
	
	while modified:
		i+=1
		modified=False
		print(i)
		for nt in regles:
			for prod in regles[nt]:
				if not prod[1:]:
					if prod[0] in nonterminaux:
						modified=True
						singulier=prod[0]
						proba1=regles[nt][prod]
						for p in regles[singulier]:
							cnf[nt][p] += regles[singulier][p]*proba1
						
						del cnf[nt][prod]
						
						
						
		
		regles=cnf
		cnf=deepcopy(cnf)
	
	for nt in cnf:	
		sumproba=0
		for prod in cnf[nt]:
			if len(prod) < 2 and prod[0] in nonterminaux:
				raise ValueError("No cigar :",nt,prod)
			else:
				sumproba += cnf[nt][prod]
		
		#print(sumproba)
		if not (sumproba==1.0):
			raise ValueError(sumproba)
	
	return terminaux,nonterminaux, cnf

if __name__ == '__main__':
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
#	argumenteur.add_argument(
#		"-y",
#		"--yaml",
#		action='store_true',
#		default=False,
#		help="Cette option permet de mettre la sortie au format YAML"
#	)
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
	rightside=defaultdict(lambda : defaultdict(int))
	leftside =defaultdict(int)
	nonterminaux=set()
	terminaux=set()
	
	with codecs.open(args.input, 'r', 'utf-8') as entree:
		for ligne in entree:
			phrase=""
			numero=None
			if not ligne.startswith('('):
				(nomcorpus_numero, phrase) = ligne.split('\t')
				(nomcorpus, numero) = nomcorpus_numero.rpartition('_')[::2]
			
			else:
				phrase=ligne
		
		
			arbre=evaluation.defoliate(evaluation.readtree(evaluation.tokenize(phrase))[0])
			n,t = evaluation.nodesandleaves(arbre)
			nonterminaux.update(n)
			terminaux.update(t)
			
			productions=evaluation.getchildren(arbre)
		
			for elem in productions:
				leftside[elem] += len(productions[elem])
				for prod in productions[elem]:
					rightside[elem][prod] += 1
		
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
		
	
	#print(set(terminaux) & set(nonterminaux))
	grammaire=CNF(terminaux, nonterminaux,rightside)
	
	#print(grammaire)


