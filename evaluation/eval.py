#!/usr/bin/python
#-*- encoding: utf-8 -*-


import sys

from fileinput import input

#Inspiré du lecteur de S-expressions de lis.py de P. Norvig
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


args=sys.argv[1:]

for line in input(args):
	line=line.decode("utf-8")
	print readtree(line.replace('(',' ( ').replace(')',' ) ').split())

