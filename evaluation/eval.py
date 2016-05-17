#!/usr/bin/python
#-*- encoding: utf-8 -*-


import sys

from fileinput import input

#Inspiré du lecteur de S-expressions de lis.py de P. Norvig
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
def getleaves(tree):
	leaves=[]
	# print tree
	for elem in tree[1:]:
		if isinstance(elem,list):
			leaves+=getleaves(elem)
		else:
			leaves.append(elem)
	
	return leaves
		
args=sys.argv[1:]

for line in input(args):
	line=line.decode("utf-8")
	print getleaves(readtree(line.replace('(',' ( ').replace(')',' ) ').split())[0]  )

