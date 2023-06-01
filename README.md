# Simplification de surfaces triangulées

Ce projet a pour but de simplifier, compresser des surfaces en trois dimensions. Pour cela nous utilisons l'algorithme décrit dans ***Surface Simplification Using Quadric Error Metrics*** de *[Michael Garland](https://www.cs.cmu.edu/afs/cs/user/garland/www/home.html)* et *[Paul S. Heckbert](https://www.cs.cmu.edu/~ph/)* dans le cadre du programme de recherche de l'université [Carnegie Mellon](https://www.cmu.edu/).

## Installations nécessaires

Pour le bon fonctionnement du programme, il faut installer les modules suivant avec la commande `pip install packageName` ou
`python3 -m pip install packageName`

* numpy
* polyscope
* heapq
* math
* tqdm
* time

## Utilisation 

Il suffit de lancer le fichier main.py avec python3.
Le fichier main.py contient un exemple d'utilisation de la fonction de simplification de surface.
Entre les lignes 20 et 23, il y a les différents fichiers objets que l'on peut charger.
Il suffit de décommenter celui que l'on veut simplifier et commenter les autres.

La fonction de simplification va demander un taux de simplification puis va ensuite afficher la surface simplifiée.
Ce taux de simplification est un nombre entre 0 et 100.
Il correspond au pourcentage de sommets que l'on souhaite enlever dans la surface simplifiée.

## Résumé de l'algorithme

La méthode décrite dans l'article ne permet que de simplifier des **surfaces triangulées**.
Et voici les différentes étapes :
1. Approximer l'erreur **Q** de chaque sommet à l'aide de quadriques.
2. Sélectionner les paires de sommet valides.
3. Calculer la contraction optimale de chaque paire, et la nouvelle erreur **Q** de la fusion des deux sommets devient le *coût* de contraction de la paire.
4. Placer les paires dans un tas en fonction de l'erreur avec celles ayant la plus petite en haut.
5. Supprimer les paires ayant le plus petit coût, et mettre à jour les coûts impliquants les sommets supprimés.

## Résultats 


