import polyscope as ps
import numpy as	np
from wavefront import *
import math

ps.init()
obj = load_obj( 'test_cube.obj')


# `verts` is a Nx3 numpy array of vertex positions
# `faces` is a Fx3 array of indices, or a nested list
# verts=np.array([[1.,0.,0.],[0.,1.,0.],[-1.,0.,0.],[0.,-1.,0.],[0.,0.,1.]])
# faces=[[0,1,2,3],[1,0,4],[2,1,4],[3,2,4],[0,3,4]]
#ps.register_surface_mesh("my mesh", verts, faces )
# bdry  = obj.numpy_boundary_edges()
# ps_net= ps.register_curve_network("boundary", obj.only_coordinates(), bdry )

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

def prodVect(v1, v2):
    res = [0, 0, 0]

    return res

tab = vect([3,5,2],[8,1,3])
print(tab)

############ Etape 2 ############

t = 0  # threshold
valid_pairs = []  # list of valid pairs


# if v1 and v2 are connected by an edge return true
def is_edge(v1, v2):
    # Check if vertices share the same x, y, or z coordinate value
    if v1[0] == v2[0] and v1[1] == v2[1]:
        # Check if distance between vertices is equal to edge length
        if math.isclose(abs(v1[2] - v2[2]), 2):
            return True
    elif v1[1] == v2[1] and v1[2] == v2[2]:
        if math.isclose(abs(v1[0] - v2[0]), 2):
            return True
    elif v1[0] == v2[0] and v1[2] == v2[2]:
        if math.isclose(abs(v1[1] - v2[1]), 2):
            return True
    return False

def all_valid_pairs(obj, t):
    # compare each pair of vertices and chek if they are valid
    for v1 in obj.vertices:
        for v2 in obj.vertices:
            if v1 != v2 and is_edge(v1, v2) or np.linalg.norm(np.subtract(v1, v2)) < t:
                valid_pairs.append((v1, v2))

all_valid_pairs(obj, t)
print("valid pairs")
# print(valid_pairs)



####################################


# remove the vertex v1 from the mesh
def remove_vertex(obj, vertex_index):
    # Remove the vertex from the vertex list
    obj.vertices = np.delete(obj.vertices, vertex_index, 0) 


# supprime une face
# remove_vertex(obj, 0)
    
ps_mesh = ps.register_surface_mesh("spot", obj.only_coordinates(), obj.only_faces() )
#ps.show()

L = obj.ordered_boundary()
print(L)