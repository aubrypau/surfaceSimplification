# surfaceSimplification

Simplification de surfaces triangulées via la méthode Surface simplification using quadric error metric de Garland et Heckbert.

-- Installations nécessaires --
numpy
polyscope
heapq
math
tqdm
time

-- Utilisation --

Il suffit de lancer le fichier main.py avec python3.
Le fichier main.py contient un exemple d'utilisation de la fonction de simplification de surface.
Entre les lignes 20 et 23, il y a les différents fichiers objets que l'on peut charger.
Il suffit de décommenter celui que l'on veut simplifier et commenter les autres.

La fonction de simplification va demander un taux de simplification puis va ensuite afficher la surface simplifiée.
Ce taux de simplification est un nombre entre 0 et 100.
Il correspond au pourcentage de sommets que l'on souhaite enlever dans la surface simplifiée.

-- Fonctionnement --

Pour simplifier une surface, nous avons utilisé la méthode 'Surface simplification using quadric error metric' de Garland et Heckbert.
Cette méthode consiste à calculer une métrique d'erreur pour chaque sommet de la surface.
Cette métrique d'erreur est calculée en fonction de la distance entre le sommet et ses voisins.
On place ensuite chaque couple sommet-voisin dans un tas en fonction de sa métrique d'erreur.
On fusionne ensuite chaque couple en les retirant du tas et en recalculant la métrique d'erreur du sommet résultant de la fusion.
On répète cette opération jusqu'à ce que le nombre de sommets de la surface soit égal au nombre de sommets souhaité.
