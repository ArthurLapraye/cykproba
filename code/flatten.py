#!/usr/bin/python3
#-*- encoding: utf-8 -*-

import re

def flatten2(tree):
	l=list()
	for elem in tree:
		if isinstance(elem, list):
			if "↓" in elem[0]:	
				l+=flatten2(elem[1:])
			else:
				l.append(flatten2(elem))
		else:
			l.append(elem)
	
	return l
	
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
	print(flatten(['SENT', ['NP-SUJ', ['DET', "'Cette'"], ['NC', "'exposition'"]], ['PONCT↓Ssub-MOD↓PONCT↓PONCT↓VN↓NP-OBJ↓PONCT', ['PONCT', "','"], ['Ssub-MOD↓PONCT↓PONCT↓VN↓NP-OBJ↓PONCT', ['Ssub-MOD', ['CS', "'comme'"], ['Sint', ['VN↑V', "'devait'"], ['VPinf-OBJ', ['VN↑VINF', "'conclure'"], ['NP-OBJ', ['NPP', "'Roger'"], ['NPP', "'Thiriot'"]]]]], ['PONCT↓PONCT↓VN↓NP-OBJ↓PONCT', ['PONCT', "','"], ['PONCT↓VN↓NP-OBJ↓PONCT', ['PONCT', '\'"\''], ['VN↓NP-OBJ↓PONCT', ['VN', ['ADV', "'n''"], ['V', "'a'"]], ['NP-OBJ↓PONCT', ['NP-OBJ', ['DET', "'d''"], ['ADJ↓NC↓Ssub', ['ADJ', "'autre'"], ['NC↓Ssub', ['NC', "'ambition'"], ['Ssub', ['CS', "'que'"], ['PP', ['P', "'d''"], ['VPinf', ['VN↑VINF', "'apporter'"], ['NP-OBJ', ['DET', "'un'"], ['ADJ↓NC↓PP', ['ADJ', "'modeste'"], ['NC↓PP', ['NC', "'témoignage'"], ['PP', ['P', "'sur'"], ['NP', ['DET', "'le'"], ['NC↓PP', ['NC', "'passé'"], ['PP', ['P+D', "'du'"], ['NP', ['NC', "'tissu'"], ['AP↓PP', ['AP↑ADJ', "'économique'"], ['PP', ['P', "'de'"], ['NP', ['DET', "'la'"], ['NC', "'région'"]]]]]]]]]]]]]]]]]], ['PONCT', "'.'"]]]]]]]]
)	)

