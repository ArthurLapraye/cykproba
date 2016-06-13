#!/usr/bin/python3
#-*- encoding: utf-8 -*-
#Arthur Lapraye - 2016


import codecs

def tokenize(string):
	""" Tokenise une S-expression. """
	return string.replace('(',' ( ').replace(')',' ) ').split()

def readtree(tokens):
	"""
	Fonction inspirée du lecteur de S-expressions de lis.py de P. Norvig http://norvig.com/python-lisp.html
	Prend une liste de tokens tirée d'un fichier parenthésé et renvoie la liste python correspondante.
	(SENT (NP (V bla) (VP (V bli)))) => ['SENT', ['NP', ['V', 'bla'], ['VP', ['V', 'bli']]]]
	"""
	if tokens == []:
		raise SyntaxError('unexpected EOF while reading')
	token = tokens.pop(0)
	if '(' == token:
		L = []
		while tokens[0] != ')':
			L.append(readtree(tokens))
		tokens.pop(0) # pop off ')'
		return L
	elif ')' == token:
		raise SyntaxError('unexpected )')
	else:
		return token

def getleaves(tree):
	"""
	Renvoie la liste des feuilles d'un arbre obtenu avec la fonction readtree.
	['SENT', ['NP', ['V', 'bla'], ['VP', ['V', 'bli']]]] => ['bla','bli']
	"""
	leaves=[]
	# print tree
	for elem in tree[1:]:
		if isinstance(elem,list):
			leaves+=getleaves(elem)
		else:
			leaves.append(elem)
	
	return leaves
	
def defoliate(tree):
	"""Supprime les feuilles d'un arbre et remplace les dernières branches par des feuilles
	"""
	newtree=list()
	newtree.append(tree[0])
	
	for elem in tree[1:]:
		if isinstance(elem, list):
			if not isinstance(elem[1],list): #elem[1] in getleaves(tree)
				newtree.append(elem[0])
			else:
				newtree.append(defoliate(elem))
	
	return newtree

def getspans(tree):
	"""
	Prend en entrée un arbre de constituants tel que produit par readtree et une position de départ dans la phrase, par défaut 0
	Renvoie une liste de tuples contenant l'étiquette du constituant et son span dans la phrase : (étiquette, début, fin)
	 ['SENT', ['NP', ['V', 'bla'], ['VP', ['V', 'bli']]]] =>
	 [('bla', 0, 1), ('V', 0, 1), ('bli', 1, 2), ('V', 1, 2), ('VP', 1, 2), ('NP', 0, 2), ('SENT', 0, 2)]
	"""
	def getsp(tree,offset):
		spans=list()
		beginoffset=offset
		# print(tree)
		for elem in tree[1:]:
			if isinstance(elem,list):
				sp,of= getsp(elem,offset)
				spans += sp
				offset = of
			else:
				spans.append( (elem,offset,offset+1) )
				offset += 1
		
	
		spans.append((tree[0],beginoffset,offset))
	
		return spans,offset
	
	return getsp(tree,0)[0]

def goodconst(spans1,spans2,verbose=False):
	"""
	Compare les constituants de deux arbres en fonction de leurs constituants communs
	Deux constituants sont identiques s'ils ont le même nom et le même span.
	Les constituants communs aux deux arbres sont comptabilisés dans la variable correct
	Les constituants de tree1 absent de tree2 sont comptabilisés dans err1
	Les constituants de tree2 absents de tree1 sont comptabilisés dans err2
	"""
	correct,err1,err2=0.0,0.0,0.0
	badspans=list()
	
	for elem in spans1:
		if elem in spans2:
			correct += 1
			spans2.pop(spans2.index(elem))
		else:
			err1 += 1
			badspans.append(elem)
		
	if verbose:
		print(badspans)
		print(spans2)
	
	err2+=len(spans2)
	
	return correct,err1,err2

def unlabel(spans):
	"""Fonction qui retire les étiquettes des spans de constituants
	   Utilisée pour mesurer précision, rappel et f-mesure non-étiquetés 
	"""
	return [(y,z) for x,y,z in spans]

if __name__ == "__main__":
	import sys
	import fileinput as fi
	from optparse import OptionParser
	
	#Options du script
	usage=u"""Usage : {0} --gold fichiergold fichier ou cat fichier | {0} --gold fichiergold
	""".format(sys.argv[0])
	
	p = OptionParser(usage=usage)
	
	p.add_option("-g","--gold", 
					action="store",
					dest="gold", 
					default=None,
					help=u"Localisation du fichier contenant les phrases gold.")
	
	p.add_option("-l","--labeled",
					action="store_true",
					dest="labeled",
					default=False,
					help=u"Si cette option est activée, la comparaison des constituants tiendra compte de leur étiquette.")
	
	p.add_option("-v","--verbose",
					action="store_true",
					dest="verbose",
					default=False,
					help=u"Option pour imprimer des détails sur le fonctionnement du script.")
	
	
	(op,args)=p.parse_args()
	LABELED=op.labeled
	VERBOSE=op.verbose
	
	#Le script a obligatoirement besoin d'un fichier de phrases gold en paramètre
	#Sinon il ne marche pas
	if op.gold:
		with codecs.open(op.gold, encoding="utf-8") as goldilocks:
			
			#Variables pour calculer précision, rappel et fmesure globaux			
			globcorr,globerr1,globerr2=float(),float(),float()
			#Variables pour calculer précision, rappel et fmesure moyens
			sumprec,sumrapp,sumfmes=float(),float(),float()
			i=0
			
			#On considère que chaque ligne du fichier gold comprend  
			
			for (pred,gold) in zip(fi.input(args),goldilocks):
				pred=pred #.decode("utf-8")
				golg=gold #.decode("utf-8")
				
				#On retire les feuilles des arbres
				predtree=readtree(tokenize(pred))[0]
				goldtree=readtree(tokenize(gold))[0]
				
				i += 1
				
				#Liste de spans de constituants qui servent à établir le comptage
				goldspans=getspans(goldtree)
				predspans=getspans(predtree)
				
				#Si les calculs se font sur des spans non-étiquetés, il faut retirer les étiquettes
				if not LABELED:
					goldspans=unlabel(goldspans)
					predspans=unlabel(predspans)
				
				
				goldleaves=getleaves(goldtree)
				predleaves=getleaves(predtree)
				
				#La comparaison entre les spans de constituants 
				#Ne peut être pertinente que si elle se fait sur la même phrase
				if goldleaves == predleaves:
					
					#Corr contient le nombre de constituants communs aux deux arbres
					#Err1 contient le nombre de constituants présents uniquement dans le gold
					#Err2 contient le nombre de constituants présents uniquement dans l'arbre prédit
					if VERBOSE:
						print(i," : ",goldleaves)
					
					corr,err1,err2=goodconst( goldspans, predspans,verbose=VERBOSE)
					
					#Il faut soustraire du nombre de constituants communs le nombre de feuilles
					#Sinon on fait gonfler artificiellement le score
					corr -= len(goldleaves)
					
					#print corr, err1,err2
					
					precision=(corr / (corr+err2))
					rappel = (corr / (corr+err1))
					fmesure = (precision*rappel*2.0)/(precision+rappel)
					
					globcorr += corr
					globerr1 += err1
					globerr2 += err2
					
					sumprec += precision
					sumrapp += rappel
					sumfmes += fmesure
					
					if VERBOSE:
						print("p :",precision,"r :",rappel,"f :",fmesure)
						print()
					
		
				else:
					raise ValueError("Phrases différentes :\n"+str(goldleaves)+"\n"+str(predleaves))
					
		#Calcul de précision, rappel, et f-mesure globaux & moyens
		globprec=globcorr/(globcorr+globerr2)
		globrapp=globcorr/(globcorr+globerr1)
		print(u"précision globale :", globprec,u" précision moyenne :", sumprec/i)
		print(u"rappel global :", globrapp, u"rappel moyen :", sumrapp/i)
		print(u"fmesure globale :",(2*globrapp*globprec)/(globrapp+globprec), u"f-mesure moyenne :", sumfmes/i)
	else:
		raise RuntimeError(u"Vous avez oublié de spécifier un fichier gold !")
