import week1_2.w1w2main as last_week
# noinspection PyUnresolvedReferences
from week1_2.w1w2main import longest_path
from itertools import product
from pprint import pprint

def is_topological_ordering(ordering, graph):
    while ordering:
        last = ordering.pop(-1)
        for node in graph[last].keys():
            if node in ordering:
                return False

    return True

# Consecutive indels are scored as sigma + k*epsilon
# Returns the graph and a topological ordering
def affine_gap_graph(v, w, match, mismatch, sigma, epsilon):
    m = len(v)
    n = len(w)

    graph = {}

    for k in product(range(m+1),    range(1, n+1)): graph[(k, "upper")]  = {}
    for k in product(range(m+1),    range(n+1)):    graph[(k, "middle")] = {}
    for k in product(range(1, m+1), range(n+1)):    graph[(k, "lower")]  = {}



    # upper goes right, lower goes down, middle goes diagonally

    # Constructing upper
    for i in range(m+1):
        for j in range(1, n):
            graph[((i, j), "upper")] [((i, j+1), "upper")] = -epsilon

    # Constructing middle
    for i in range(m):
        for j in range(n):
            graph[((i, j), "middle")] [((i+1, j+1), "middle")] = match if v[i] == w[j] else -mismatch

    # Constructing lower
    for i in range(1, m):
        for j in range(n + 1):
            graph[((i, j), "lower")] [((i+1, j), "lower")] = -epsilon

    # Constructing connections from middle to upper
    for i in range(m + 1):
        for j in range(n):
            graph[((i, j), "middle")] [((i, j+1), "upper")] = -sigma

    # Constructing connections from middle to lower
    for i in range(m):
        for j in range(n + 1):
            graph[((i, j), "middle")] [((i+1, j), "lower")] = -sigma

    # Constructing connections from upper to middle
    for i in range(m + 1):
        for j in range(1, n + 1):
            graph[((i, j), "upper")] [((i, j), "middle")] = 0

    # Constructing connections from upper to middle
    for i in range(1, m + 1):
        for j in range(n + 1):
            graph[((i, j), "lower")][((i, j), "middle")] = 0

    order = []
    for i in range(m+1):
        for j in range(n+1):
            order.append(((i, j), "middle"))
            if j < n:
                order.append(((i, j+1), "upper"))
            if i < m:
                order.append(((i+1, j), "lower"))
    return graph, order

def affine_path_to_alignment(v, w, path):
    v_res = []
    w_res = []
    tail = path[0]
    cur_layer = "middle"

    for head in path[1:]:
        next_layer = head[1]
        i, j = tail[0]

        if next_layer == cur_layer:
            if cur_layer == "middle":
                v_res.append(v[i])
                w_res.append(w[j])
            elif cur_layer == "upper":
                v_res.append("-")
                w_res.append(w[j])
            elif cur_layer == "lower":
                v_res.append(v[i])
                w_res.append("-")
        elif next_layer == "upper":
            v_res.append("-")
            w_res.append(w[j])
        elif next_layer == "lower":
            v_res.append(v[i])
            w_res.append("-")

        tail = head
        cur_layer = next_layer

        # Going from upper or lower to middle does nothing

    print(v_res)
    print(w_res)
    return "".join(v_res), "".join(w_res)



def affine_alignment(v, w, match, mismatch, sigma, epsilon):
    graph, order = affine_gap_graph(v, w, match, mismatch, sigma, epsilon)

    path, score = longest_path(graph, order)

    return *affine_path_to_alignment(v, w, path), score
