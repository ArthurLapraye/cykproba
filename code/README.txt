
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

II - Le script ckys.py
	
	I.1
		Le script ckys.py se lance avec deux arguments. 
		Le premier est un pickle contenant une PCFG sous forme normale de Chomsky produite par le script extracteur.py.
		Le deuxième argument est un corpus, un fichier mrg contenant les phrases que le script devra analyser.
			
		ckys.py grammaire_train.pickle test.mrg 
	
		Par défaut, le script est lancé de façon non-interactive : 
		il traite toutes les phrases du corpus en commençant par la première et imprime l'analyse sur 
		stdin et des messages d'informations ou d'erreur sur stderr.
	
	I.2 Options
		
		I.2.1 L'option -i
			
			L'option -i permet de lancer le script en mode interactif
			Le mode interactif affiche chaque phrase une par une avec leur longueur et leur numéro, 
			ainsi que des commandes de l'utilisateur 
				Les commandes acceptées par le script sont les suivantes :
				
					exit,
					quit ,
					Ctrl+D : quitte le script
					
					y : lance l'analyse de la phrase courante
					
					goto NOMBRE : va à la phrase numéro NOMBRE si NOMBRE est plus grand que le numéro de la phrase actuelle
					
		I.2.2 L'option -p
			
			L'option p donne la position de départ dans le corpus du script. 
			Par défaut le script commence au début du fichier. 
			Spécifier un numéro avec l'option -p permet de le faire commencer à la phrase correspondant à ce numéro.
		
	
	

	
