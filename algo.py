import heapq

def compute_Q_matrix(vertex):
    # code to compute Q matrix for a given vertex
    pass

def compute_error(vertex, Q1, Q2):
    # code to compute the error of the given vertex
    pass

# Step 1: Compute the Q matrices for all the initial vertices.
vertices = [...]  # list of initial vertices
Q_matrices = {v: compute_Q_matrix(v) for v in vertices}

# Step 2: Select all valid pairs.
valid_pairs = [...]  # list of valid pairs

# Step 3: Compute the optimal contraction target v ̄ for each valid pair (v1 , v2 ).
#          The error v ̄ T (Q1 + Q2 )v ̄ of this target vertex becomes the cost of contracting that pair.
costs = {}
for v1, v2 in valid_pairs:
    Q1, Q2 = Q_matrices[v1], Q_matrices[v2]
    v_bar = ...  # code to compute the optimal contraction target
    error = compute_error(v_bar, Q1, Q2)
    costs[(v1, v2)] = error

# Step 4: Place all the pairs in a heap keyed on cost with the minimum cost pair at the top.
heap = [(cost, pair) for pair, cost in costs.items()]
heapq.heapify(heap)

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
