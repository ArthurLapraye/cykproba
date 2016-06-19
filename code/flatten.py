#!/usr/bin/python3
#-*- encoding: utf-8 -*-

import re

def flatten2(tree):
	

	
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
	pass
	#return flatten2(flatten1(tree))



if __name__=="__main__":
	
	print(flatten2( ['SENT', ['PP-MOD', ['P', "'Pour'"], ['NP', ['DET', "'ce'"], ['ADJ↓NC', ['ADJ', "'premier'"], ['NC', "'rendez-vous'"]]]], ['PONCT↓NP-SUJ↓VN↓VPinf-OBJ↓COORD↓PONCT', ['PONCT', "','"], ['NP-SUJ↓VN↓VPinf-OBJ↓COORD↓PONCT', ['NP-SUJ', ['DET', "'l''"], ['NC', "'animateur'"]], ['VN↓VPinf-OBJ↓COORD↓PONCT', ['VN', ['V', "'a'"], ['VPP↓VINF', ['VPP', "'pu'"], ['VINF', "'faire'"]]], ['VPinf-OBJ↓COORD↓PONCT', ['VPinf-OBJ', ['VN↑VINF', "'partager'"], ['NP-OBJ', ['DET', "'sa'"], ['NC', "'passion'"]]], ['COORD↓PONCT', ['COORD', ['CC', "'et'"], ['VN↓NP-OBJ↓PP-DE_OBJ', ['VN↑VINF', "'présenter'"], ['NP-OBJ↓PP-DE_OBJ', ['NP-OBJ', ['DET', "'quelques'"], ['PONCT↓NC↓PONCT', ['PONCT', '\'"\''], ['NC↓PONCT', ['NC', "'oeuvres'"], ['PONCT', '\'"\'']]]], ['PP-DE_OBJ', ['P', "'pour'"], ['VPinf', ['VN↑VINF', "'mettre'"], ['PP-P_OBJ↓NP-OBJ', ['PP-P_OBJ', ['P', "'en'"], ['NP↑NC', "'bouche'"]], ['NP-OBJ', ['DET', "'les'"], ['NC', "'participants'"]]]]]]]], ['PONCT', "'.'"]]]]]]] ))
	
	['SENT', ['PP-MOD', ['P', "'Pour'"], ['NP', ['DET', "'ce'"], ['ADJ↓NC', ['ADJ', "'premier'"], ['NC', "'rendez-vous'"]]]], ['PONCT', "','"], 'NP-SUJ↓VN↓VPinf-OBJ↓COORD↓PONCT', ['NP-SUJ', ['DET', "'l''"], ['NC', "'animateur'"]], ['VN', ['V', "'a'"], ['VPP', "'pu'"], 'VINF', "'faire'"], 'VPinf-OBJ↓COORD↓PONCT', ['VPinf-OBJ', ['VN↑VINF', "'partager'"], ['NP-OBJ', ['DET', "'sa'"], ['NC', "'passion'"]]], ['COORD', ['CC', "'et'"], ['VN↑VINF', "'présenter'"], 'NP-OBJ↓PP-DE_OBJ', ['NP-OBJ', ['DET', "'quelques'"], ['PONCT↓NC↓PONCT', ['PONCT', '\'"\''], ['NC↓PONCT', ['NC', "'oeuvres'"], ['PONCT', '\'"\'']]]], ['PP-DE_OBJ', ['P', "'pour'"], ['VPinf', ['VN↑VINF', "'mettre'"], ['PP-P_OBJ↓NP-OBJ', ['PP-P_OBJ', ['P', "'en'"], ['NP↑NC', "'bouche'"]], ['NP-OBJ', ['DET', "'les'"], ['NC', "'participants'"]]]]]], 'PONCT', "'.'"]

