# Projet IA QUIXO

Thomas Vandermeersch - 17030  
Landry Taymans - 17046

## Bibliothèques utilisées :

* cherrypy
* sys
* random

## Stratégie de l'IA :

Avant de jouer, l'IA analyse tous les coups qui lui sont possible de 
jouer. Elle choisit ensuite le coup qui lui permet de faire la plus 
grande ligne possible. Si deux coups on une ligne maximale de même 
taille, l'IA regarde pour lequel des deux, le joueur adverse, à la 
plus courte ligne maximale.

Pour ne pas entrer dans une boucle infinie de même coup, avant de jouer, 
l'IA regarde également si le joueur adverse et elle-même ont 
respectivement fait plus de trois fois le même coup d'affilé. Si c'est 
le cas, elle choisit un autre coup pour débloquer la situation. 
Cependant, si ce coup permet à l'adversaire de marquer un ligne de plus 
de quatre, l'IA préférera rester dans une boucle infinie.
