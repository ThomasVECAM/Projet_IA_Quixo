# Projet IA QUIXO

Thomas Vandermeersch - 17030  
Landry Taymans - 17046

## Langage utilisé :

Python 3.6

## Bibliothèques utilisées :

* cherrypy
* sys
* Random (pour *matches.py* qui joue en aléatoire)

## Stratégie de l'IA :

Avant de jouer, l'IA analyse tous les coups qui lui sont possibles de 
jouer pour ce tour. Elle choisit ensuite le coup qu'elle considère comme 
le meilleur (en suivant les critères cités ci-dessous).

1. Si le coup lui permet de faire une suite de 5 et qu'il ne provoque 
pas une ligne de 5 chez l'adversaire, elle joue ce coup.

1. Si le coup amène l'adversaire à une suite de 4, elle passe au coup 
suivant.

1. Elle vérifie qu'elle n'est pas dans une boucle infinie de même coup 
en analysant le dictionnaire des précédants coups jouer par elle et son 
adversaire. Si elle est dans une boucle, elle passera au coup suivant. 
*L'IA préférera rester dans une boucle infinie plutôt que de faire 
gagner l'adversaire*

1. L'IA regarde ensuite le coup qui lui permet de faire la plus grande 
ligne possible.

1. Si deux coups on une ligne maximale de même taille, l'IA regarde pour 
lequel des deux, le joueur adverse, à la plus courte ligne maximale.
