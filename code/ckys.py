#!/usr/bin/python3
# coding: utf8


def CYKmaker(gr):
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
					raise ValueError("Production invalide :",p)
	
	def cyk(u) :
		T=dict()
	
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
			
		for i in range(2,len(u)+1):
			for y in range(1,(len(u)-i+2)) :
				span=(y,i+y)
				print(span)
				for j in range(y+1,i+y) :
					cds=T[(j,i+y)]
					print("\t",(y,j),(j,i+y))	
															  
					for (a,b) in T[(y,j)],key=lambda x : T[(y,j)][x]:
						z=(a,b)
						pa=T[y,j][z]
																
						if a in debuts:
							suite=debuts[a]
							for (c,d) in cds:
								pz=pa*cds[c,d]
								if c in suite:
									r=(z,(c,d))
								
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
			#for (a,b) in list(T.keys()):
			#	if (b-a) == i-3:
				#print(T[a,b])
			print(i)	
			#input()
		
		return T
	
	return cyk

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

	parsing=CYKmaker(cnf[2])
	
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
			
			
			
			z=parsing(phrase)
			#affiche_arbre(z,phrase)
			print(treemaker(z,phrase))


if __name__ == '__main__':
	import cProfile
	cProfile.run("main()")
