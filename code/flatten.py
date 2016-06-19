#!/usr/bin/python3
#-*- encoding: utf-8 -*-

import re

def flatten2(tree):
	if len(tree)==3:
		head,leftchild,rightchild=tree
		l=[head,flatten2(leftchild)]
		if "↓" in rightchild[0]:
			for elem in flatten2(rightchild)[1:]:
				l.append(elem)
			
			return l
		else:
			l.append(flatten2(rightchild))
			return l
	
	elif len(tree) == 2:
		return tree
			

def flatten1(tree):
	if len(tree) == 3:

		head,leftchild,rightchild=tree
	
		if "↑" in head:
			g,d=re.split("↑",head,1)
			return [g,flatten([d,leftchild,rightchild]) ]
		else:
			return [head,flatten1(leftchild),flatten1(rightchild)]
		
	elif len(tree) == 2:
		head,child=tree
		if "↑" in head:
			g,d=re.split("↑",head,1)
			return [g,flatten1([d,child]) ]
		else:
			return [head,child]
			
	else:
		raise ValueError("Nombre de branches incorrect pour :",tree)
	
def flatten(tree):
	return flatten2(flatten1(tree))

if __name__=="__main__":
	pass

