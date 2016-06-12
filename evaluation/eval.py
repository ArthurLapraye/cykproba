#!/usr/bin/python
#-*- encoding: utf-8 -*-
#Arthur Lapraye - 2016


import codecs
from pprint import pprint

def tokenize(string):
	""" Tokenise une S-expression """
	return string.replace('(',' ( ').replace(')',' ) ').split()

def readtree(tokens):
	"""
	Inspiré du lecteur de S-expressions de lis.py de P. Norvig http://norvig.com/python-lisp.html
	Prend une liste de tokens tirée d'un fichier parenthésé et renvoie la liste python correspondante
	"""
	if len(tokens) == 0:
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
	Renvoie la liste des feuilles d'un arbre obtenu avec la fonction readtree
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
	"""Supprime les feuilles d'un arbre et remplace les dernières branches par des feuilles"""
	newtree=list()
	newtree.append(tree[0])
	
	for elem in tree[1:]:
		if isinstance(elem, list):
			if elem[1] in getleaves(tree):
				newtree.append(elem[0])
			else:
				newtree.append(defoliate(elem))
	
	return newtree

def getspans(tree):
	"""
	Prend en entrée un arbre de constituants tel que produit par readtree et une position de départ dans la phrase, par défaut 0
	Renvoie une liste de tuples contenant l'étiquette du constituant et son span dans la phrase
	"""
	def getsp(tree,offset):
		spans=list()
		beginoffset=offset
		# print tree
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
		print spans2
		print badspans
	
	err2+=len(spans2)
	
	return correct,err1,err2

def unlabel(spans):
	"""Fonction qui retire les étiquettes des spans de constituants
	   Utilisée pour mesurer précision, rappel et f-mesure non-étiquetés 
	"""
	return [(y,z) for x,y,z in spans]
	 

if __name__ == "__main__":
	import sys
	from fileinput import input
	
	from optparse import OptionParser
	
	usage="""Usage : prend comme argument un fichier mrg.strict ou bien un pipe depuis stdin
	./eval.py $fichier est équivalent à cat $fichier | ./eval.py
	"""
	
	p = OptionParser(usage=usage)
	
	p.add_option("-g","--gold", 
					action="store",
					dest="gold", 
					default=None,
					help=u"Localisation du fichier contenant les phrases gold.")
	
	(op,args)=p.parse_args()
	#args=sys.argv[1:]
	if op.gold:
		with codecs.open(op.gold, encoding="utf-8") as goldilocks:
		
			globcorr,globerr1,globerr2=float(),float(),float()
			sumprec,sumrapp,sumfmes=float(),float(),float()
			i=0
			
			for (pred,gold) in zip(input(args),goldilocks):
				pred=pred.decode("utf-8")
				golg=gold #.decode("utf-8")
				predtree=defoliate(readtree(tokenize(pred))[0])
				goldtree=defoliate(readtree(tokenize(gold))[0])
				
				i += 1
				
				print i," : "
				#pprint(goldtree)
				#pprint(predtree)
				print getleaves(goldtree)
				print getleaves(predtree)
				
				goldspans=getspans(goldtree)
				predspans=getspans(predtree)
				if getleaves(goldtree) == getleaves(predtree):
					
					corr,err1,err2=goodconst( goldspans, predspans) #if labeled else goodspans(gold,pred)
		
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
					
					print precision,rappel,fmesure
					
		
				else:
					raise ValueError("Phrases différentes :\n"+str(gold).encode("utf-8")+"\n"+str(pred).encode("utf-8"))
				
				
				print
				
		globprec=globcorr/(globcorr+globerr2)
		globrapp=globcorr/(globcorr+globerr1)
		print u"précision globale :", globprec,u" précision moyenne :", sumprec/i
		print u"rappel global :", globrapp, u"rappel moyen :", sumrapp/i
		print u"fmesure globale :",(2*globrapp*globprec)/(globrapp+globprec), u"f-mesure moyenne :", sumfmes/i
	else:
		raise RuntimeError(u"Vous avez oublié de spécifier un fichier gold !")

#TODO : accomoder des forêts d'analyse partagée (?) (à voir en amont)

