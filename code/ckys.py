#!/usr/bin/python3
# coding: utf8


def CYKmaker(cnf):
	"""
		Fonction qui construit le dictionnaire inverse des productions
			Pour une règle
				a -> b,c
		Le dictionnaire a une entrée
			b -> c -> a -> prob
		Ce qui accélère le traitement.
		
		La fonction CYK proprement dite est incluse dans cette fonction, afin de ne pas devoir reconstruire
		le dictionnaire inverse à chaque fois : ce dernier est inclus dans la clôture lexicale de CYKmaker.
	"""
	terminaux,nonterminaux,gr=cnf
	debuts=dict()
	
	#Construction du dictionnaire inverse des productions
	#à partir de la grammaire
	for n in gr:
		for p in gr[n]:
			if len(p) == 2:
				if not p[0] in debuts:
					debuts[p[0]]=dict()
				if p[1] not in debuts[p[0]]:
					debuts[p[0]][p[1]]= dict()
					debuts[p[0]][p[1]][n]= float(gr[n][p])
				else:
						#print(n,p)
					if n in debuts[p[0]][p[1]]:
						print("Warning :",n,"=>",p, gr[n][p] )
					
					debuts[p[0]][p[1]][n] = float( gr[n][p] )
			
			else:
				#Si la grammaire n'est pas en CNF
				if len(p) >  1 or p[0] not in terminaux:
					raise ValueError("Production invalide :",p)
	
	#Fonction CYK proprement dite	
	def cyk(u,verbose=False) :
		"""
			Fonction de parsing ascendant CYK probabiliste.
			Prend en entrée une phrase et renvoie un tableau rempli avec les réécritures possibles.
		"""
		T=dict()
		
		#Remplissage du premier rang du tableau
		#Utilisation des règles unaires.	
		for i in range(1,len(u)+1) :
		#On parcourt le mot à reconnaitre
			for l in gr :	
				for r in gr[l]:														   
				#On parcourt la grammaire
					if (u[i-1] == r[0] ):														  
					#Si la lettre en cours est identique à une partie droite de règle
						if (i,i+1) not in T :
							T[(i,i+1)]=dict()
						if l not in T[i,i+1]:
							T[i,i+1][l]=dict()
							
						if r not in T[(i,i+1)][l]:
							T[(i,i+1)][l][(r,)] = float(gr[l][r])										
							 #On remplit la case
						else : 
							T[(i,i+1)][l][(r,)] += float( gr[l][r] )										   
							#On rajoute une autre règle s'il y en a + qu'une
			
			if (i,i+1) not in T :
				T[(i,i+1)]=[]															  
				#Si une case est vide, on ajoute un tableau vide dedans pour qu'elle apparaisse dans le dico
		
		
		#Remplissage des rangs supérieurs du tableau
		for i in range(2,len(u)+1):
			
			for y in range(1,(len(u)-i+2)) :
				span=(y,i+y)
				#print(span)
				for j in range(y+1,i+y) :
					
					#print("\t",(y,j),(j,i+y))	
					sp1=(y,j)
					sp2=(j,i+y)
					cds=T[sp2]
					
					#						  
					for a in T[(y,j)]:
						if a in debuts:
								suite=debuts[a]
								for c in cds:
									if c in suite:
										r=((a,sp1),(c,sp2))
										recrits=suite[c]
										
										for z in T[y,j][a]:
											pa=T[y,j][a][z]
											for d in cds[c]:
												pz=pa*cds[c][d]
												for l in recrits:
													pb=recrits[l]
													newpb= pz*pb
									
													if span not in T:
														T[span]=dict()
													if l not in T[span]:
														T[span][l]=dict()
													if r not in T[span][l]:
														T[span][l][r] = newpb
													else:
														T[span][l][r] += newpb
				
				
				if span not in T :
					T[span]=dict()
			
			if verbose:
				print(i)	
		
		return T
	
	return cyk

def treemaker(T,u):
	"""
		Fonction de backtracking pour extraire le meilleur arbre de la charte CYK.
	"""
	longueur=len(u)
	
	def maketree(Z):
		retour=[]
		for tup in Z:
			if len(tup) > 1:
				Y=sorted(T[tup[1]][tup[0]],key= lambda x : (T[tup[1]][tup[0]][x]) ,reverse=True )
				Z=Y[0]
				if len(Y) > 1:
					if T[tup[1]][tup[0]][Z] == T[tup[1]][tup[0]][Y[1]]:
						print(Y,Z)
				
				if len(Z) == 1:
					retour.append([tup[0],Z[0][0]])
				else:
					next=[tup[0] ]
					for child in maketree(Z):
						next.append(child)
					retour.append(next)
			else:
				retour.append(tup[0])
		
		return retour

	maxprob=0
	maxZ=[]
	maxelem=None
	for elem in T[1,1+longueur]:
		if elem.startswith("SENT"):
			Z=max(T[1,1+longueur][elem],key=lambda x : (T[1,1+longueur][elem][x] ))
			
			newprob=T[1,1+longueur][elem][Z]
			
			if newprob > maxprob:
				maxprob=newprob
				maxZ=Z
				maxelem=elem
			elif newprob == maxprob:
				if len(elem) < len(maxelem):
					maxelem=elem
					maxZ=Z
			
	return [maxelem]+maketree(maxZ)



if __name__ == '__main__':
	from extracteur import defaultdictmaker
	from collections import defaultdict
	import fractions
	
	import pickle
	import evaluation
	import sys, codecs
	
	from argparse import ArgumentParser
	from flatten import flatten
	
	import re
	import logging
	logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
	
	argu=ArgumentParser(prog="ckys.py",
						description="""Implémentation d'un parser CYK probabiliste 
						prenant en entrée une PCFG et un corpus de phrases MRG"""
						
						)
	argu.add_argument("fichiergrammaire",
						metavar="grammaire",
						help="""Le fichier de grammaire est un pickle produit par extracteur.py
							""")
	
	argu.add_argument("corpus",metavar="corpus",help="""Le deuxième argument contient le corpus au format MRG.""")
	
	argu.add_argument('-i','--inter', 
						dest='interactif', 
						action='store_true',
						default=False,
						help="""Si cette option est active le script fonctionne en mode interactif.""")
	
	args=argu.parse_args()
	
	with open(args.fichiergrammaire, 'rb') as fichiergrammaire:
		cnf = pickle.load(fichiergrammaire)

	parse=CYKmaker(cnf)
	
	i=0
	
	with codecs.open(args.corpus, "r") as corpus:
		for phrase in corpus:
			i+=1
			if not phrase.startswith('('):
				(nomcorpus_numero, phrase) = phrase.split('\t')
				(nomcorpus, numero) = nomcorpus_numero.rpartition('_')[::2]
			arbre=evaluation.readtree(evaluation.tokenize(phrase))[0]
			
			phrase = evaluation.getleaves(arbre)
			
			if args.interactif:
				print("n°",i)
				print("Longueur de la phrase :",len(phrase))
				print("phrase : ", re.sub(r"'([^']+)'",r"\1"," ".join(phrase)) )
				try:
					goon=input()
				except EOFError:
					break
				if goon == "quit" or goon == "exit":
					break
				elif goon == "y":
					z=parse(phrase,verbose=True)
					print(evaluation.writetree(flatten(treemaker(z,phrase))))
					print()
				else:
					continue
			
			else:
				logging.info("phrase numéro"+str(i)+"traitée")
				print("("+evaluation.writetree(flatten(treemaker(parse(phrase),phrase)))+")")



