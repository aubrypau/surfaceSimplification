import polyscope as ps
import numpy as np
from wavefront import *
import math
import heapq
import time

THRESHOLD_T = 0
MINIMUM_FACES = 10

ps.init()

obj = load_obj('mesh/hourglass_ico.obj')
# obj = load_obj( 'mesh/spot.obj')              # vache
# obj = load_obj( 'mesh/tet.obj')               # pyramide
# obj = load_obj( 'mesh/test_cube.obj')         # cube
# obj = load_obj( 'mesh/feline_half.obj')       # feline



# `verts` is a Nx3 numpy array of vertex positions
# `faces` is a Fx3 array of indices, or a nested list
# verts=np.array([[1.,0.,0.],[0.,1.,0.],[-1.,0.,0.],[0.,-1.,0.],[0.,0.,1.]])
# faces=[[0,1,2,3],[1,0,4],[2,1,4],[3,2,4],[0,3,4]]
# ps.register_surface_mesh("my mesh", verts, faces )
# bdry  = obj.numpy_boundary_edges()
# ps_net= ps.register_curve_network("boundary", obj.only_coordinates(), bdry )


############ Etape 1 ############
# Step 1: Compute the Q matrices for all the initial vertices.

# je pense ca marche plus j'ai chengé is_edge
def getAllEdges(v1):
    tab = []
    for v2 in obj.vertices:
        if v1 != v2:
            if is_edge(v1, v2):
                tab.append((v2))
    return tab


def getAllFaces(v1):
    tab = []
    tabv2 = getAllEdges(v1)


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

def normeVect(v):
    return math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)


tab = prodVect([1, 1, 1], [2, 1, 1])
print(tab)
norme = normeVect(tab)
print(norme)


############ Etape 2 ############

t = 0  # threshold
valid_pairs = []  # list of valid pairs


# if v1 and v2 are connected by an edge return true
def is_edge(v1, v2):
    for f in obj.only_faces():
        if v1 in f and v2 in f:
            return True
    return False


def all_valid_pairs(obj):
    # compare each pair of vertices and chek if they are valid
    for v1 in obj.vertices:
        for v2 in obj.vertices:
            if v1 != v2 and is_edge(v1, v2) or np.linalg.norm(np.subtract(v1, v2)) < THRESHOLD_T:
                valid_pairs.append((v1, v2))


# all_valid_pairs(obj, t)
# print("valid pairs")
# print(valid_pairs)


####################################


# remove the vertex v1 from the mesh
def remove_vertex(obj, vertex_index):
    # Remove the vertex from the vertex list
    obj.vertices = np.delete(obj.vertices, vertex_index, 0)

def get_all_neighbours(obj, vertex_index):
    neighbours = []
    for v in range (0, len(obj.vertices)):
        if is_edge(vertex_index, v) and vertex_index != v:
            neighbours.append(v)
    return neighbours

def remove_faces(obj, face_index):
    # Remove the face from the face list
    # print(obj.only_faces())
    for f in obj.only_faces():
        if face_index in f:
            print("removed face")
            print(f)
            print("face index")
            print(obj.polygons)
            if obj.polygons[face_index] 

# print("neighbours")
# print(get_all_neighbours(obj, 10))


remove_vertex(obj, 7)
# remove_vertex(obj, 8)

remove_faces(obj, 7)


# print(obj.only_faces())


# v
# print(obj.vertices)

# vn
# print(obj.normals)

# vt
# print(obj.texcoords)

    
ps_mesh = ps.register_surface_mesh("spot", obj.only_coordinates(), obj.only_faces() )
ps.show()

L = obj.ordered_boundary()
print(L)
