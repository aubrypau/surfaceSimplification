# Simplification de surfaces triangulées

Ce projet a pour but de simplifier, compresser des surfaces en trois dimensions.

Pour cela nous utilisons l'algorithme décrit dans ***Surface Simplification Using Quadric Error Metrics*** de *[Michael Garland](https://www.cs.cmu.edu/afs/cs/user/garland/www/home.html)* et *[Paul S. Heckbert](https://www.cs.cmu.edu/~ph/)* dans le cadre du programme de recherche de l'université [Carnegie Mellon](https://www.cmu.edu/).

## Résumé de l'algorithme

La méthode décrite dans l'article ne permet que de simplifier des **surfaces triangulées**.
Et voici les différentes étapes :
1. Approximer l'erreur **Q** de chaque sommet à l'aide de quadriques.
2. Sélectionner les paires de sommet valides.
3. Calculer la contraction optimale de chaque paire, et la nouvelle erreur **Q** de la fusion des deux sommets devient le *coût* de contraction de la paire.
4. Placer les paires dans un tas en fonction de l'erreur avec celles ayant la plus petite en haut.
5. Supprimer les paires ayant le plus petit coût, et mettre à jour les coûts impliquants les sommets supprimés.

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

Le fichier [wavefront.py](wavefront.py) contient les fonctions nécessaires à la lecture et l'écriture de fichiers `.obj`. Nous en avons rajouté quelques une adaptées à notre besoin.

Le fichier [main.py](main.py) contient le code permettant de simplifier une surface triangulée. Dans celui-ci nous retrouvons toutes les [étapes](Résumé de l'algorithme) décrites précédement.

Le dossier [Mesh](/Mesh) contient tous les fichiers `.obj`.

Pour simplifier une surface, il faut choisir le modèle que l'on veut simplifier, pour cela, il faut commenter ou décommenter les lignes nécessaires entre la 20 et 23 du fichier [main.py](main.py).

Il suffit ensuite de lancer le fichier main.py avec la commande `python3 main.py`.

La programme va alors demander un taux de simplification, il faut en choisir un entre 0 (pour afficher le modèle original) et 99, qui correspond au pourcentage de sommet que l'on veut enlever. La surface simplifiée sera alors affichée après tous les calculs.

## Résultats et discussions

Octopus vertex : 2092

Octopus 25% vertex : 1569

Octopus 25% time : 37.03 s

Octopus 50% vertex : 1046

Octopus 50% time : 76.11 s

Octopus 75% vertex : 522

Octopus 75% time : 125.11 s

Bunny vertex : 502

Bunny 25% vertex : 376

Bunny 25% time : 2.40 s

Bunny 50% vertex : 251

Bunny 50% time : 4.76 s

Bunny 75% vertex : 125

Bunny 75% time : 7.26 s

![lapin](/readme_assets/bunny.png)
<img src="/readme_assets/octopus.png" width="100" height="100">

| Taux de compression | 0% | 25% | 50% | 75% |
| --------------------|----|-----|-----|-----|
| Bunny | <img src="/readme_assets/bunny.png"> | <img src="/readme_assets/bunny25.png"> | <img src="/readme_assets/bunny50.png"> | <img src="/readme_assets/bunny75.png">
| Octopus | <img src="/readme_assets/octopus.png" width="100" height="100"> | <img src="/readme_assets/octopus25.png" width="100" height="100"> | <img src="/readme_assets/octopus50.png" width="100" height="100"> | <img src="/readme_assets/octopus75.png" width="100" height="100">


