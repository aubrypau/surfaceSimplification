import polyscope as ps
import numpy as np
from wavefront import *
import math
import heapq
import time
from tqdm import tqdm

THRESHOLD_T = 0
MINIMUM_FACES = 5
LABEL = []
COORDONNEES = []
FACES = []
VOISINS = []
NB_SOMMETS = 0
Qs = []

ps.init()

# Choix de l'objet à charger (décommenter l'objet souhaité)

# obj = load_obj("Mesh/hourglass_ico.obj")      # hourglass
obj = load_obj("Mesh/octopus.obj")            # octopus
# obj = load_obj( 'Mesh/lapin.obj')             # lapin



def init_label():
    global LABEL
    for i in range(len(obj.vertices)):
        LABEL.append(i)


def init_coordonnees():
    global COORDONNEES
    for i in range(len(obj.vertices)):
        COORDONNEES.append(obj.only_coordinates()[i])


def init_faces():
    global FACES
    for i in range(len(obj.polygons)):
        FACES.append(obj.only_faces()[i])


def init_voisins():
    global VOISINS
    VOISINS = get_all_neighbours(obj)


def getAllEdges(v1):
    tab = []
    for v2 in obj.vertices:
        if v1 != v2:
            if is_edge(v1, v2):
                tab.append((v2))
    return tab


# En donnant le numéro du sommet, on récupère toutes les faces qui le contiennent
def getAllFaces(v1):
    allFaces = obj.only_faces()
    tab = []
    for f in allFaces:
        if v1 in f:
            tab.append(f)
    return tab



############ Calculer a b c d pour un plan ############

"""
Soit un tirangle PRQ, avec P le sommet, calcul les vecteurs PR et PQ
"""


# avec P le point P et p le point R ou Q
def vect(P, p):
    res = []
    for i in range(0, 3):
        res.append(p[i] - P[i])
    return res


# calcul le produit de deux vecteur
def prodVect(u, v):
    res = [0, 0, 0]
    res[0] = u[1] * v[2] - u[2] * v[1]
    res[1] = u[2] * v[0] - u[0] * v[2]
    res[2] = u[0] * v[1] - u[1] * v[0]
    return res


# permet de calculer la norme d'un vecteur (distance)
def normeVect(v):
    return math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)


# calcul un produit vectorielle divisé par sa norme
def prodVectNormed(u, a):
    res = []
    for i in range(3):
        res.append(u[i] / a)
    return res


# calcul du prolduit entre le vecteur n et P (l'origine du triangle)
def scalarProduct(n, P):
    nb = 0
    for i in range(3):
        nb += n[i] * P[i]
    return nb


def matrixABCDfromPoints(P, Q, R):
    PR = vect(P, R)
    PQ = vect(P, Q)

    PQPR = prodVect(PQ, PR)
    norme = normeVect(PQPR)

    n = prodVectNormed(PQPR, norme)

    d = scalarProduct(n, P) / norme
    n.append(d)
    return n


# abcd = matrixABCDfromPoints(P, Q, R)

############ Etape 2 ############


# if v1 and v2 are connected by an edge return true
def is_edge(v1, v2):
    allEdgesV1 = obj.getAllEdgesOfVertex(v1)
    for e in allEdgesV1:
        if e == v2:
            return True
    return False


def get_all_neighbours(obj):
    all_neighbours = []
    print("Compute all neighbours")
    tb = time.time()
    for v in tqdm(range(0, len(obj.vertices))):
        all_neighbours.append(obj.getAllEdgesOfVertex(v))
    print('time:', time.time() - tb, "\n")
    return all_neighbours


def all_valid_pairs(obj):
    global VOISINS
    print("Compute the valids pairs")
    tb = time.time()
    valid_pairs = []
    for v1 in tqdm(range(0, len(obj.vertices))):
        for voisin in VOISINS[v1]:
            if v1 < voisin:
                valid_pairs.append((v1, voisin))
    print('time:', time.time() - tb, "\n")
    return valid_pairs


####################################


# Récupère les faces d'un sommet puis calcule la matrice pour chaque face
def getAllABCDfromVertex(vNumber):
    f = getAllFaces(vNumber)
    abcd = []

    # On récupère ensuite les coordonnées des sommets obtenus
    for i in range(len(f)):
        P = obj.get_coord(f[i][0])
        R = obj.get_coord(f[i][1])
        Q = obj.get_coord(f[i][2])
        abcd.append(matrixABCDfromPoints(P, Q, R))

    return abcd


def getAllKfromVertex(vNumber):
    Kp = []
    ABCDs = getAllABCDfromVertex(vNumber)

    for i in range(len(ABCDs)):
        matrice_initiale = np.matrix(ABCDs[i])
        matrice_ligne = np.reshape(matrice_initiale, (1, 4))
        matrice_colonne = np.reshape(matrice_ligne, (4, 1))
        Kp.append(matrice_colonne * matrice_ligne)

    return Kp


def Q(vNumber):
    Kp = getAllKfromVertex(vNumber)

    Q = Kp[0]
    # Calcul la somme des erreurs
    for i in range(1, len(Kp)):
        Q += Kp[i]

    return Q


def quadraticError(v, Q):
    return v.T * Q * v


def moyPointContraction(v1, v2):
    res = [0, 0, 0]

    for i in range(3):
        res[i] = (v1[i] + v2[i]) / 2

    return res


def errorContractionV(v1, v2):
    global Qs
    coorV1 = obj.get_coord(v1)
    coorV2 = obj.get_coord(v2)
    Q1 = Qs[v1]
    Q2 = Qs[v2]

    coorV3 = moyPointContraction(coorV1, coorV2)
    Q3 = Q1 + Q2

    V3 = [coorV3[0], coorV3[1], coorV3[2], 1]
    V3 = np.matrix(V3).T

    q3 = quadraticError(V3, Q3)

    resErr = q3

    return resErr, (v1, v2)

# Renvoi la position du point de contraction qui minimise l'erreur quadratique
def posContractionV(v1, v2):
    global Qs

    coorV1 = obj.get_coord(v1)
    coorV2 = obj.get_coord(v2)
    Q1 = Qs[v1]
    Q2 = Qs[v2]

    coorV3 = moyPointContraction(coorV1, coorV2)
    Q3 = Q1 + Q2

    V1 = [coorV1[0], coorV1[1], coorV1[2], 1]
    V1 = np.matrix(V1).T

    V2 = [coorV2[0], coorV2[1], coorV2[2], 1]
    V2 = np.matrix(V2).T

    V3 = [coorV3[0], coorV3[1], coorV3[2], 1]
    V3 = np.matrix(V3).T

    q1 = quadraticError(V1, Q1)
    q2 = quadraticError(V2, Q2)
    q3 = quadraticError(V3, Q3)

    if q1 < q2 and q1 < q3:
        resPos = coorV1
    elif q2 < q1 and q2 < q3:
        resPos = coorV2
    else:
        resPos = coorV3
    return resPos


# permet de calculer toutes les matrices Q pour touts les sommets
def calculateAllQ():
    print("Calcul de toutes les matrices Q")
    res = []
    vertex = obj.only_coordinates()
    tb = time.time()
    for i in tqdm(range(len(vertex))):
        res.append(Q(i))
    print("time: ", time.time() - tb, "\n")
    return res



def computeContraction(validPairs):
    cost = []
    tb = time.time()
    for i in tqdm(range(len(validPairs))):
        cost.append(errorContractionV(validPairs[i][0], validPairs[i][1]))
    print("time: ", time.time() - tb, "\n")
    return cost


def convertContractionToHeap(tab):
    res = []
    for i in range(len(tab)):
        res.append([tab[i][0].item(), tab[i][1]])
    return res


# Tri le tas
def heapsort(iterable):
    h = []
    while iterable:
        y = heapq.heappop(iterable)
        h.append([y[0], y[1]])
    return h


####### Gestion des labels ########

def label(i):
    global LABEL
    while i != LABEL[i]:
        i = LABEL[i]
    return i

def union(i, j):
    global LABEL
    LABEL[label(i)] = label(j)

###################################

def getCoord(i):
    global COORDONNEES
    return COORDONNEES[label(i)]

def editCoord(i, coord):
    global COORDONNEES
    COORDONNEES[i] = coord

def nbLabels():
    res = []
    for i in range(len(LABEL)):
        if i == label(i):
            res.append(i)
    return len(res)


def getPairsWithV1(heap, v):
    res = []
    for i in range(len(heap)):
        if heap[i][1][0] == v or heap[i][1][1] == v:
            res.append(i)
    return res


def updatePairsWithV1(heap, list):
    for i in range(len(list)):
        heap[list[i]][0] = errorContractionV(label(heap[list[i]][1][0]), label(heap[list[i]][1][1]))[
            0
        ].item()


# suppression des paires qui peuvent être fusionnées après une contraction
def delete_same_pair(heap, v1, v2):
    res = []
    pairv1 = getPairsWithV1(heap, v1)
    pairv2 = getPairsWithV1(heap, v2)
    for pair in pairv1:
        if heap[pair][1][0] == v1:
            for pair2 in pairv2:
                if (heap[pair][1][1] == heap[pair2][1][0]) or (heap[pair][1][1] == heap[pair2][1][1]):
                    if not(pair in res):
                        res.append(pair)
            if not(pair in res):
                heap[pair][1] = (v2, heap[pair][1][1])
        else:
            for pair2 in pairv2:
                if (heap[pair][1][0] == heap[pair2][1][0]) or (heap[pair][1][0] == heap[pair2][1][1]):
                    if not(pair in res):
                        res.append(pair)
                if not(pair in res):
                    heap[pair][1] = (heap[pair][1][0], v2)
    return res



####### Programme principal ########

def main(simplification):
    global Qs
    if simplification != 0 and simplification < 100:

        debut = time.time()

        global NB_SOMMETS, LABEL, Qs, COORDONNEES
        # initialisation
        print("\n###### Surfaces Simplification ######")
        print("\nStep 1 - Initialisation")
        init_label()
        NB_SOMMETS = len(LABEL)
        print("\nVertex number : ", NB_SOMMETS, "\n")
        init_coordonnees()
        init_faces()
        init_voisins()

        # Compute the Q matrices for all the initial vertices
        print("Step 2 - Compute the Q matrices for all the initial vertices")
        Qs = calculateAllQ()

        # Compute the valid pairs
        print("Step 3 - Compute the valid pairs")
        valid_pairs = all_valid_pairs(obj)

        # Compute the cost of each contraction
        print("Step 4 - Compute the cost of each contraction")
        res = computeContraction(valid_pairs)

        # Place all the pairs in a heap keyed on cost with the minimum cost pair at the top
        print("Step 5 - Place pairs in the heap")
        trt = time.time()
        heapTab = convertContractionToHeap(res)
        heapq.heapify(heapTab)
        heapTab = heapsort(heapTab)
        print("time: ", time.time() - trt, "\n")

        # Iteratively remove the pair (v1 , v2 ) of least cost from the heap, contract this pair, and update the costs of all valid pairs involving v1.
        print("Step 6 - Removing pairs")
        tb = time.time()
        taux_simplification = (NB_SOMMETS / 100) * simplification
        nb_simplification = 0
        pbar = tqdm(total=nb_simplification)
        while nb_simplification < taux_simplification and nb_simplification < NB_SOMMETS - MINIMUM_FACES:
            
            pair = heapq.heappop(heapTab)
            v1 = label(pair[1][0])
            v2 = label(pair[1][1])

            # Axiome
            if (v1 == v2):
                raise SystemExit('\n Error: Contraciton de deux point deja contracté !! \n')

            # Calcul des nouvelles coordonnées
            editCoord(v2, posContractionV(v1, v2))

            # Contraciton
            union(v1, v2)

            # Calcul de la nouvelle matrice Q
            Qs[v2] = Qs[v1] + Qs[v2]

            # Supprime les pairs en double
            pair_to_del = delete_same_pair(heapTab, v1, v2)
            pair_to_del.reverse()
            for i in pair_to_del:
                heapTab.pop(i)

            # update des pairs impliquant v1 et v2
            updatePairsWithV1(heapTab, getPairsWithV1(heapTab, v1))
            updatePairsWithV1(heapTab, getPairsWithV1(heapTab, v2))

            # Axiome
            if ( nbLabels() != NB_SOMMETS-nb_simplification-1):
                raise SystemExit('\n Error: Le nombre de sommets n\' est pas proportionel au nombre de simplification effectué \n')

            # Tri du tas
            heapq.heapify(heapTab)
            heapTab = heapsort(heapTab)

            # Axiome
            for i in range(len(heapTab)-1):
                if heapTab[i][0] > heapTab[i+1][0]:
                    raise SystemExit('\n Error: Tas non trié !! \n')

            nb_simplification += 1
            
            pbar.update(1)
            pbar.set_description("Simplification : %i" % nb_simplification)
            
        print("\ntime: ", time.time() - tb, "\n")

        finLabel = []
        for lbl in LABEL:
            if label(lbl) not in finLabel:
                finLabel.append(label(lbl))


        ps_Coord = []
        for i in range(len(COORDONNEES)):
            ps_Coord.append(COORDONNEES[label(i)])
        ps_Coord = np.array(ps_Coord)

        ps_Faces = FACES

        print("\nVertex number after simplification : ",len(LABEL)-nb_simplification, "\n")

        ps_register = ps.register_surface_mesh("spot", ps_Coord, ps_Faces)

        fin = time.time()

        print("\n Total execution time : ", fin - debut, "\n")
        ps.show()

    else:

        print("\nObject without simplification")
        print("\nVertex number : ", len(obj.only_coordinates()), "\n")
        ps_register = ps.register_surface_mesh(
            "spot", obj.only_coordinates(), obj.only_faces()
        )
        ps.show()


if __name__ == "__main__":
    taux = input(
        "\nEnter the compression ratio ( 0 for the orignal object ) : \n"
    )
    main(int(taux))
