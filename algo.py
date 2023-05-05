import heapq
import numpy as np

def compute_Q_matrix(vertex):
    x, y, z = vertex[0], vertex[1], vertex[2]
    Q = np.array([[0,0,0,0],
                  [0,0,0,0],
                  [0,0,0,0],
                  [x, y, z, 1]])
    return Q

def compute_error(vertex, Q1, Q2):
    return 0

def isEdge(v1, v2):
    return True


############################################################################################################
# Step 1: Compute the Q matrices for all the initial vertices.


vertices = [...]  # list of initial vertices
Q_matrices = {v: compute_Q_matrix(v) for v in vertices}


############################################################################################################
# Step 2: Select all valid pairs. 
# pair is valid if :  
#       (v1,v2) is an edge or ||v1 - v2|| < t 

t = 0  # threshold
valid_pairs = [...]  # list of valid pairs

# compare each pair of vertices and chek if they are valid
for v1 in vertices:
    for v2 in vertices:
        if v1 != v2 and isEdge(v1, v2) or np.linalg.norm(v1 - v2) < t:
            valid_pairs.append((v1, v2))




############################################################################################################
# Step 3: Compute the optimal contraction target v ̄ for each valid pair (v1 , v2 ).
#          The error v ̄ T (Q1 + Q2 )v ̄ of this target vertex becomes the cost of contracting that pair.
costs = {}
for v1, v2 in valid_pairs:
    Q1, Q2 = Q_matrices[v1], Q_matrices[v2]
    v_bar = ...  # code to compute the optimal contraction target
    error = compute_error(v_bar, Q1, Q2)
    costs[(v1, v2)] = error


############################################################################################################
# Step 4: Place all the pairs in a heap keyed on cost with the minimum cost pair at the top.
heap = [(cost, pair) for pair, cost in costs.items()]
heapq.heapify(heap)


############################################################################################################
# Step 5: Iteratively remove the pair (v1 , v2 ) of least cost from the heap, contract this pair, 
#         and update the costs of all valid pairs involving v1.
while heap:
    cost, (v1, v2) = heapq.heappop(heap)
    Q1, Q2 = Q_matrices[v1], Q_matrices[v2]
    v_bar = ...  # code to compute the optimal contraction target
    # code to contract the pair (v1, v2) and update the Q matrices
    for v in vertices:
        if v != v1 and v != v2 and (v, v1) in valid_pairs:
            Q_matrices[v] += Q1
            new_cost = compute_error(v_bar, Q_matrices[v], Q_matrices[v1])
            costs[(v, v1)] = new_cost
            heapq.heappush(heap, (new_cost, (v, v1)))
        if v != v1 and v != v2 and (v1, v) in valid_pairs:
            Q_matrices[v] += Q1
            new_cost = compute_error(v_bar, Q_matrices[v], Q_matrices[v1])
            costs[(v1, v)] = new_cost
            heapq.heappush(heap, (new_cost, (v1, v)))
        if v != v1 and v != v2 and (v, v2) in valid_pairs:
            Q_matrices[v] += Q2
            new_cost = compute_error(v_bar, Q_matrices[v], Q_matrices[v2])
            costs[(v, v2)] = new_cost
            heapq.heappush(heap, (new_cost, (v, v2)))
        if v != v1 and v != v2 and (v2, v) in valid_pairs:
            Q_matrices[v] += Q2
            new_cost = compute_error(v_bar, Q_matrices[v], Q_matrices[v2])




