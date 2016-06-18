#!/usr/bin/python3
# coding: utf8

# Representations de deux grammaires

g1 = [('S', 'AB'), ('S', 'a'), ('A', 'SB'), ('A', "b"), ('B', 'b')]
g2 = [('S', 'AS'), ('S', 'b'), ('A', 'a')]

def getAxiom(gr) :
	return gr[0][0]

# --------------------------#
# Base de l'algorithme CYK  #
# --------------------------#



#Initialisation de la table T pour le mot u et la grammaire gr

def init(T, u, gr) :
	for i in range(1,len(u)+1) :													
	#On parcourt le mot à reconnaitre
		for l in gr :	
			for r in gr[l]:														   
			#On parcourt la grammaire
				if (u[i-1] == r[0] ):														  
				#Si la lettre en cours est identique à une partie droite de règle
					if (i,i+1) not in T :
						T[(i,i+1)]=dict()
						T[(i,i+1)][l,r[0]] = float(gr[l][r])										
						 #On remplit la case
					else : 
						T[(i,i+1)][l,r[0] ]= T[(i,i+1)].get( (l,r[0] ) ,0) + float( gr[l][r] )										   
						#On rajoute une autre règle s'il y en a + qu'une
		if (i,i+1) not in T :
			T[(i,i+1)]=[]															  
			#Si une case est vide, on ajoute un tableau vide dedans pour qu'elle apparaisse dans le dico
	return T


"Remplissage de la table T (initialisation deja  effectuee) pour le mot u et la grammaire gr"

def boucle(T,u,gr) :

	debuts=dict()
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
				if p[0][0] != "'":
					print(p)
					input()
			
	for i in range(2,len(u)+1):
	#On utilise y et i pour parcourir la chart
		for y in range(1,(len(u)-i+2)) :
			span=(y,i+y)
			print(span)
			for j in range(y+1,i+y) :
				cds=T[(j,i+y)]												  
			#La variable j est utilisée pour trouver la moitié du protomot
				for (a,b) in T[(y,j)]:
					z=(a,b)
					pa=T[y,j][z]											
				#On regarde dans les paires de cases nécéssaire pour remplir la prochaine
					if a in debuts:
						suite=debuts[a]
						for (c,d) in cds:
							pz=pa*cds[c,d]
							if c in suite: #debuts[a]:
								r=((a,b),(c,d))
								#print(r)
								recrits=suite[c]
								for l in recrits:
									
									pb=recrits[l]
									
									newpb= pz*pb
									
									if span not in T:
										T[span]=dict()
										T[span][l,r]=newpb 
									else:
										if (l,r) not in T[span]:
											T[span][l,r] = newpb
										else:
											#print(l,r)
											T[span][l,r] += newpb
											#input()		  
				
				
				#print(j)
				
			if span not in T :
				#print("*")
				T[span]=dict()
				
			#print(y)
		
		print(i)	
		
	return T


"Analyse du mot u pour la grammaire gr"

def parsing(gr,u) :
	T = dict()#{}
	init(T, u, gr)
	boucle(T, u, gr)
	return T

def affiche_arbre(T, u) :
	if True :
		chaine = ""
		for i in range(1,len(u)+2) :
			chaine = ""
			for j in range(1,i) :
				x = j
				y = len(u)+2-i+j
				chaine = chaine + "\t".join([z[0] for z in T[x,y]]) + " "
			print (chaine)
	print

def treemaker(T,u):
	longueur=len(u)
	for elem in sorted(T[1,1+longueur],key=lambda x: T[1,1+longueur][x] ) :
		if elem[0].startswith("SENT"):
			print(elem)

from extracteur import defaultdictmaker

def main():
	
	from collections import defaultdict
	import fractions
	
	import pickle
	import evaluation
	import sys, codecs

	with open(sys.argv[1], 'rb') as fichiergrammaire:
		cnf = pickle.load(fichiergrammaire)

	with codecs.open(sys.argv[2], "r") as corpus:
		for phrase in corpus:
			if not phrase.startswith('('):
				(nomcorpus_numero, phrase) = phrase.split('\t')
				(nomcorpus, numero) = nomcorpus_numero.rpartition('_')[::2]
			arbre=evaluation.readtree(evaluation.tokenize(phrase))[0]
			phrase = evaluation.getleaves(arbre)
			print("phrase : ", phrase)
			print(len(phrase))
			
			goon=input()
			if goon == "":
				continue
			if goon == "quit":
				break
			
			
			z=parsing(cnf[2],phrase)
			#affiche_arbre(z,phrase)
			print(treemaker(z,phrase))


if __name__ == '__main__':
	import cProfile
	cProfile.run("main()")
