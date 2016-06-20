
Manuel utilisateur pour le projet CYK probabiliste.

I - Exemple 
	
	Cette section présente de façon rapide l'ensemble des scripts du projet CYK probabiliste.
	En lançant les commandes présentées dans l'ordre, on obtient successivement 
	un corpus d'entraînement et de test, une grammaire tirée du corpus d'entraînement
	un ensemble de parse candidats et enfin leur évaluation vis-à-vis du corpus de test.

	Étant donné un fichier mrg fi.mrg :
	
	I.1
	
		La commande : 
	
			dispatch.py fi.mrg train.mrg test.mrg 
		
		crée deux fichiers, 
			train.mrg, qui doit servir de corpus d'entraînement (90 % de fi.mrg)
			test.mrg qui doit servir de corpus de test (10% de fi.mrg )
		
			(La répartition entre les deux fichiers est faite au hasard)
	
	I.2
	
		La commande 
		
			extracteur.py fi.mrg grammaire.pickle 
		
		extrait une PCFG (sous forme normale de Chomsky) à partir de fi.mrg et l'enregistre dans le fichier grammaire.pickle
	
			extracteur.py train.mrg grammaire_train.pickle 
		
		extrait une PCFG à partir de train.mrg et l'enregistre dans le fichier grammaire_train.pickle
	
	I.3
	
		La commande
	
			updategrammar.py grammaire.pickle grammaire_train.pickle 
		
		modifie le fichier grammaire_train.pickle : elle sert à transférer dans la grammaire d'entraînement l'ensemble des 
		règles lexicales du corpus afin d'éviter d'avoir des erreurs dues à des mots inconnus 
		
	I.4
		
		La commande 
			
			ckys.py grammaire_train.pickle test.mrg > sortie_test.mrg 
			
		Lance l'analyse des phrases de test.mrg par CYK probabiliste et les rassemble dans sortie_test.mrg
		ATTENTION : cette étape peut durer extrêmement longtemps (plusieurs heures). 
		Pour voir rapidement le fonctionnement de cky, utiliser le "mode interactif" (cf ci-dessous).
	
	I.5
		La commande 
			
			evaluation.py --gold test.mrg sortie_test.mrg 
		
		Calcule précision, rappel et f-mesure non-étiquetés sur sortie_test.mrg en prenant pour référence les parses originaux
		dans test.mrg.


	
