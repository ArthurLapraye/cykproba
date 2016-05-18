#!/usr/bin/python
#-*- encoding: utf-8 -*-
#Arthur Lapraye - 2016

import sys

from fileinput import input

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
	#newtree.append(tree[0])
	for elem in tree:
		if isinstance(elem, list):
			if len(elem) > 2:
				newtree.append(defoliate(elem))
			else:
				newtree.append(elem[0])
		else:
			newtree.append(elem)
	
	return newtree

def getspans(tree,offset=0):
	"""
	Prend en entrée un arbre de constituants tel que produit par readtree et une position de départ dans la phrase, par défaut 0
	Renvoie une liste de tuples contenant l'étiquette du constituant et son span dans la phrase
	"""
	spans=list()
	beginoffset=offset
	# print tree
	for elem in tree[1:]:
		
		if isinstance(elem,list):
			sp,of= getspans(elem,offset)
			spans += sp
			offset = of
		else:
			spans.append( (elem,offset,offset+1) )
			offset += 1
		
	
	spans.append((tree[0],beginoffset,offset))
	
	return spans,offset


args=sys.argv[1:]

if __name__ == "__main__":
	"""
	Usage : prend comme argument un fichier mrg.strict, en lit le contenu et imprime les résultats des fonctions defoliate et getleaves
	Ainsi que le span de chaque noeud de l'arbre syntaxique, y compris les terminaux, triés dans l'ordre linéaire
	"""
	for line in input(args):
		line=line.decode("utf-8")
		tree=readtree(line.replace('(',' ( ').replace(')',' ) ').split())[0] 
		leaves=getleaves(tree)
		spans=getspans(tree)[0]

		print
		print leaves
		print defoliate(tree)
		for const,i,j in sorted(spans,key=lambda (x,y,z) : z):
			print const.encode("utf-8"),leaves[i:j]

