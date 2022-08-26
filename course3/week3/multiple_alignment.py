from itertools import product
from week1_2.w1w2main import longest_path

def path_to_alignment(path, *args):
    tail = path[0]
    n = len(args)
    res = [[] for i in range(n)]

    for head in path[1:]:
        vect = [head[i] - tail[i] for i in range(n)]
        for i in range(n):
            if vect[i] == 0:
                res[i].append("-")
            elif vect[i] == 1:
                res[i].append(args[i][tail[i]])

        tail = head

    return list("".join(alignment) for alignment in res)


def LCS_multi_graph(u, v, w, indel=0, mismatch=0, match=1, face=0):
    l = len(u)
    m = len(v)
    n = len(w)

    graph = {k: {} for k in product(range(l+1), range(m+1), range(n+1))}

    for x, y, z in product(range(l), range(m), range(n)):
        graph[(x, y, z)] [(x + 1, y, z)] = -indel
        graph[(x, y, z)] [(x, y + 1, z)] = -indel
        graph[(x, y, z)] [(x, y, z + 1)] = -indel

        graph[(x, y, z)][(x + 1, y + 1, z)] = face
        graph[(x, y, z)][(x + 1, y, z + 1)] = face
        graph[(x, y, z)][(x, y + 1, z + 1)] = face

        graph[(x, y, z)][(x + 1, y + 1, z + 1)] = match if u[x] == v[y] == w[z] else -mismatch

    for i in range(l):
        graph[(i, m, n)][(i+1, m, n)] = -indel

    for j in range(m):
        graph[(l, j, n)][(l, j+1, n)] = -indel

    for k in range(m):
        graph[(l, m, k)][(l, m, k+1)] = -indel

    return graph

def multi_alignment(u, v, w, match=1, mismatch=0, indel=0):
    graph = LCS_multi_graph(u, v, w, indel=indel, mismatch=mismatch, match=match)
    path, score = longest_path(graph)
    return path_to_alignment(path, u, v, w), score

