import polyscope as ps
import numpy as np
from wavefront import *
import math
import heapq


THRESHOLD_T = 0
MINIMUM_FACES = 10
LABEL = []
COORDONNEES = []
FACES = []
VOISINS = []

ps.init()

# obj = load_obj("Mesh/hourglass_ico.obj")
obj = load_obj("Mesh/bunnyhead.obj")          # octopus
# obj = load_obj( 'Mesh/spot.obj')              # vache
# obj = load_obj( 'Mesh/tet.obj')               # pyramide
# obj = load_obj( 'Mesh/test_cube.obj')         # cube
# obj = load_obj( 'Mesh/feline_half.obj')       # feline


# `verts` is a Nx3 numpy array of vertex positions
# `faces` is a Fx3 array of indices, or a nested list
# verts=np.array([[1.,0.,0.],[0.,1.,0.],[-1.,0.,0.],[0.,-1.,0.],[0.,0.,1.]])
# faces=[[0,1,2,3],[1,0,4],[2,1,4],[3,2,4],[0,3,4]]
# ps.register_surface_mesh("my mesh", verts, faces )
# bdry  = obj.numpy_boundary_edges()
# ps_net= ps.register_curve_network("boundary", obj.only_coordinates(), bdry )


def init_label():
    for i in range(len(obj.vertices)):
        LABEL.append(i)

def init_coordonnees():
    for i in range(len(obj.vertices)):
        COORDONNEES.append(obj.only_coordinates()[i])


def init_faces():
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


# Ici on récupère les faces qui contiennent le sommet numéro 12
# tab = getAllFaces(12)
# print("tab : ", tab)

# On récupère ensuite les coordonnées des sommets obtenus
# print("obj.vertices tab[0][0]: ", obj.only_coordinates()[tab[0][0]])
# print("obj.vertices tab[0][1]: ", obj.only_coordinates()[tab[0][1]])
# print("obj.vertices tab[0][2]: ", obj.only_coordinates()[tab[0][2]])

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


# test pour la matrice [ a b c d ]
P = [1, 4, 8]
R = [2, 5, 4]
Q = [6, 2, 3]

PR = vect(P, R)
# print(PR)
PQ = vect(P, Q)
# print(PQ)
PQPR = prodVect(PQ, PR)
# print(PQPR)

norme = normeVect(PQPR)
# print(norme)

n = prodVectNormed(PQPR, norme)

d = scalarProduct(n, P)
# la matrice a b c d
n.append(d / norme)
# print(n)


def matrixABCDfromPoints(P, Q, R):
    PR = vect(P, R)
    PQ = vect(P, Q)

    PQPR = prodVect(PQ, PR)
    norme = normeVect(PQPR)

    n = prodVectNormed(PQPR, norme)

    d = scalarProduct(n, P) / norme
    n.append(d)
    return n


abcd = matrixABCDfromPoints(P, Q, R)

############ Etape 2 ############

# if v1 and v2 are connected by an edge return true
def is_edge(v1, v2):
    allEdgesV1 = obj.getAllEdgesOfVertex(v1)
    for e in allEdgesV1:
        if e == v2:
            return True
    return False

# def all_valid_pairs(obj):
#     # compare each pair of vertices and chek if they are valid
#     valid_pairs = []
#     for v1 in range (0, len(obj.vertices)):
#         for v2 in range (0, len(obj.vertices)):
#             if ( (v1 != v2 and is_edge(v1, v2)) or (v1 != v2 and np.linalg.norm(np.subtract(obj.get_coord(v1), obj.get_coord(v2))) < THRESHOLD_T )):
#                 if (v1, v2) not in valid_pairs and (v2, v1) not in valid_pairs:
#                     valid_pairs.append((v1, v2))
#     print("valid_pairs : ", valid_pairs)
#     return valid_pairs

def get_all_neighbours(obj):
    all_neighbours = []
    for v in range(0, len(obj.vertices)):
        all_neighbours.append(obj.getAllEdgesOfVertex(v))
    return all_neighbours



def all_valid_pairs(obj):
    global VOISINS
    print("CAlcul des voisins")
    valid_pairs = []
    for v1 in range (0, len(obj.vertices)):
        print("v1 : ", v1)
        for voisin in VOISINS[v1]:
            if (v1 < voisin):
                valid_pairs.append((v1, voisin))
    return valid_pairs



####################################


# remove the vertex v1 from the mesh
def remove_vertex(obj, vertex_index):
    # Remove the vertex from the vertex list
    obj.vertices = np.delete(obj.vertices, vertex_index, 0)


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
    #Calcul la somme des erreurs
    for i in range(1, len(Kp)):
        Q += Kp[i]

    return  Q 

def quadraticError(v, Q):
    return v.T * Q * v

def moyPointContraction(v1, v2):
    res = [0,0,0]

    for i in range(3):
        res[i] = (v1[i] + v2[i]) / 2
    
    return res

def contractionV(v1, v2):
    global Qs
    coorV1 = obj.get_coord(v1)
    coorV2 = obj.get_coord(v2)
    Q1 = Qs[v1]
    Q2 = Qs[v2]
    
    coorV3 = moyPointContraction(coorV1, coorV2)
    Q3 = Q1 + Q2

    V1 = [ coorV1[0], coorV1[1], coorV1[2], 1]
    V1 = np.matrix(V1).T
    
    V2 = [ coorV2[0], coorV2[1], coorV2[2], 1]
    V2 = np.matrix(V2).T

    V3 = [ coorV3[0], coorV3[1], coorV3[2], 1]
    V3 = np.matrix(V3).T

    q1 = quadraticError(V1, Q1)
    q2 = quadraticError(V2, Q2)
    q3 = quadraticError(V3, Q3)

    if(q1 < q2 and q1 < q3):
        resErr = q1
        resPos = coorV1
    elif(q2 < q1 and q2 < q3):
        resErr = q2
        resPos = coorV2
    else:
        resErr = q3
        resPos = coorV3
    
    return resErr, resPos, (v1, v2)

    
    
# calculateQofVertex(4)
# print(Q(22))
# print(Q(3))

# print(getAllQfromVertex(12))
# permet de calculer toutes les matrices Q pour touts les sommets 

def calculateAllQ():
    res = []
    vertex = obj.only_coordinates()
    for i in range(len(vertex)):
        res.append(Q(i))

    return res

Qs = calculateAllQ()


def computeContraction(validPairs):
    cost = []
    for i in range(len(validPairs)):
        cost.append(contractionV(validPairs[i][0], validPairs[i][1]))
    return cost



def convertContractionToHeap(tab):
    res = []
    for i in range(len(tab)):
        res.append([tab[i][0].item(), tab[i][2]])
    return res


def heapsort(iterable):
    h = []
    for value in iterable:
        heapq.heappush(h, value[0])
    return [heapq.heappop(h) for i in range(len(h))]



# Gestion des labels

def label(i):
    while (i != LABEL[i]):
        i = LABEL[i]
    return i

def union(i, j):
    LABEL[label(i)] = label(j)

def find(i, j):
    if (label(i) == label(j)):
        return True
    else:
        return False
    
def getCoord(i):
    return COORDONNEES[label(i)]

def editCoord(i, coord):
    COORDONNEES[i] = coord

# Programme principal

def main(simplification):
    if simplification:
        # initialisation
        print("Initialisation")
        init_label()
        print(len(LABEL))
        init_coordonnees()
        init_faces()
        init_voisins()


        # Compute the Q matrices for all the initial vertices
        print("Compute the Q matrices for all the initial vertices")
        print(Qs[0])

        # Compute the valid pairs
        print("Compute the valid pairs")
        valid_pairs = all_valid_pairs(obj)

        # Compute the cost of each contraction
        print("Compute the cost of each contraction")
        res = computeContraction(valid_pairs)

        # Place all the pairs in a heap keyed on cost with the minimum cost pair at the top
        print("Place in the heap")
        heapTab = convertContractionToHeap(res)
        heapq.heapify(heapTab)
        heapsort(heapTab)
        print(heapTab)
        

        # Iteratively remove the pair (v1 , v2 ) of least cost from the heap, contract this pair, and update the costs of all valid pairs involving v1.
        # while the lowest cost contraction is greater than 5
        print("removing pairs")
        while(len(heapTab) > 700):
            pair = heapq.heappop(heapTab)
            union(pair[1][0], pair[1][1])

        # show the result of the contraction using the corresponding labels
        # print(LABEL)

        print("show the result of the contraction using the corresponding labels")
        ps_Coord = []
        for i in range(len(COORDONNEES)):
            ps_Coord.append(COORDONNEES[label(i)])
        ps_Coord = np.array(ps_Coord)

        ps_Faces = FACES

        ps_register = ps.register_surface_mesh("spot", ps_Coord, ps_Faces)
        ps.show()


    else:

        # initialisation
        print("Initialisation")
        init_label()
        print(len(LABEL))
        init_coordonnees()
        init_faces()
        init_voisins()
        print(VOISINS)
        print(all_valid_pairs(obj))


        ps_register = ps.register_surface_mesh("spot", obj.only_coordinates(), obj.only_faces())
        ps.show()

   
# main(False)
main(True)

