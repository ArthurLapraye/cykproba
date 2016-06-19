#!/usr/bin/python3
# coding: utf8


def CYKmaker(cnf):
	terminaux,nonterminaux,gr=cnf
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
				if p[0] not in terminaux:
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
		
		
		
		for i in range(2,len(u)+1):
			
			for y in range(1,(len(u)-i+2)) :
				span=(y,i+y)
				#print(span)
				for j in range(y+1,i+y) :
					
					#print("\t",(y,j),(j,i+y))	
					sp1=(y,j)
					sp2=(j,i+y)
					cds=T[sp2]
													  
					for a in T[(y,j)]:
						if a in debuts:
								suite=debuts[a]
								for c in cds:
									if c in suite:
										#r=(a,c) #(z,(c,d))
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
					#print("*")
					T[span]=dict()
				
			print(i)	
		
		return T
	
	return cyk


def printchart(T,u) :
		chaine = ""
		SYMB=["SENT"]
		NEXT=list()
		for i in range(1,len(u)+3) :
			chaine = ""
			for j in range(1,i) :
				x = j
				y = len(u)+2-i+j
				cont = None
				if (x,y) in T:
					cont = " "#(x,y)
					for e in SYMB:
						if e in T[x,y]:
							cont = e
							#SYMB=[elt for elt in T[x,y][e].keys() ]
							next =max(T[x,y][e],key=lambda z : T[x,y][e][z]) 
							print(next)
							#NEXT += list(next)
					
					SYMB=NEXT
					NEXT=list()
					
				chaine = chaine + str( cont )  + "\t"
			
			print (chaine)
		print

def treemaker(T,u):
	longueur=len(u)
	
	def maketree(Z):
		retour=[]
		for tup in Z:
			#print(offset,tup[0])
			
			if len(tup) > 1:
				Z= max(T[tup[1]][tup[0]],key= lambda x : (T[tup[1]][tup[0]][x]))
				if len(Z) == 1:
					#print(Z)
					retour.append([tup[0],Z[0][0]])
				else:
					next=[tup[0] ]
					for child in maketree(Z):
						next.append(child)
					retour.append(next)
			else:
				retour.append(tup[0])
			#	retour += [tup[0]]
				
		return retour

	maxprob=0
	maxZ=[]
	maxelem=None
	for elem in T[1,1+longueur]: #sorted(T[1,1+longueur],key=lambda x: T[1,1+longueur][x] ) :
		if elem.startswith("SENT"):
			#print(elem)
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
			
	print([maxelem]+maketree(maxZ))


if __name__ == '__main__':
	from extracteur import defaultdictmaker
	from collections import defaultdict
	import fractions
	
	import pickle
	import evaluation
	import sys, codecs

	with open(sys.argv[1], 'rb') as fichiergrammaire:
		cnf = pickle.load(fichiergrammaire)

	parsing=CYKmaker(cnf)
	
	with codecs.open(sys.argv[2], "r") as corpus:
		for phrase in corpus:
			if not phrase.startswith('('):
				(nomcorpus_numero, phrase) = phrase.split('\t')
				(nomcorpus, numero) = nomcorpus_numero.rpartition('_')[::2]
			arbre=evaluation.readtree(evaluation.tokenize(phrase))[0]
			#skeul=evaluation.getleaves(evaluation.defoliate(arbre))
			phrase = evaluation.getleaves(arbre)
			print("phrase : ", phrase)
			#print("tags : ",skeul)
			print(len(phrase))
			
			goon=input()
			if goon == "":
				continue
			if goon == "quit":
				break
			
			z=parsing(phrase)
			print(treemaker(z,phrase))



