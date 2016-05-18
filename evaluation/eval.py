#!/usr/bin/python
#-*- encoding: utf-8 -*-


import sys

from fileinput import input

#Inspiré du lecteur de S-expressions de lis.py de P. Norvig http://norvig.com/python-lisp.html
#Prend une liste de tokens tirée d'un fichier parenthésé et renvoie la liste correspondante
#
def readtree(tokens):
	
	"Read an expression from a sequence of tokens."
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

#Renvoie une liste correspondant aux feuilles d'un arbre obtenu avec la fonction readtree
#TODO : transformer en getspans pour obtenir les parties délimitées
def getleaves(tree):
	leaves=[]
	# print tree
	for elem in tree[1:]:
		if isinstance(elem,list):
			leaves+=getleaves(elem)
		else:
			leaves.append(elem)
	
	return leaves

	
def getspans(tree,offset=0):
	
	spans=dict()
	beginoffset=offset
	# print tree
	for elem in tree[1:]:
		
		if isinstance(elem,list):
			sp,of= getspans(elem,offset)
			spans.update(sp)
			offset = of
		else:
			spans[elem]=(offset,offset+1)
			offset += 1
		
	
	spans[tree[0]]=(beginoffset,offset)
	
	return spans,offset


args=sys.argv[1:]

for line in input(args):
	line=line.decode("utf-8")
	leaves=getleaves(readtree(line.replace('(',' ( ').replace(')',' ) ').split())[0]  )
	spans=getspans(readtree(line.replace('(',' ( ').replace(')',' ) ').split())[0]  )[0]
	
	
	print
	print leaves
	
	for const in spans:
		i,j=spans[const]
		print const.encode("utf-8"),leaves[i:j]

