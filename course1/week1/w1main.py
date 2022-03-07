import exercises
from itertools import product

class Graph:
    def __init__(self, adjList):
        self.adjList = adjList

    def __setitem__(self, key, value):
        self.adjList[key] = value

    def __getitem__(self, key):
        return self.adjList[key]


def manhattan_tourist_graph(down, right):
    graph = {}

    for i, row in enumerate(down):
        for j, weight in enumerate(row):
            graph[(i, j)] = {(i+1, j): weight}

    for i, row in enumerate(right):
        for j, weight in enumerate(row):
            if (i, j) not in graph:
                graph[(i, j)] = {(i, j+1): weight}
            else:
                graph[(i, j)][(i, j+1)] = weight

    return graph

def manhattan_tourist(grid, n, m):
    node_weight = {(0, 0): 0}
    for j in range(1, m+1):
        node_weight[(0, j)] = node_weight[(0, j-1)] + grid[(0, j-1)][(0, j)]

    for i in range(1, n+1):
        node_weight[(i, 0)] = node_weight[(i-1, 0)] + grid[(i-1, 0)][(i, 0)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            up   = node_weight[(i-1, j)] + grid[(i-1, j)][i, j]
            left = node_weight[(i, j-1)] + grid[(i, j-1)][i, j]

            node_weight[(i, j)] = max(up, left)

    return node_weight[(n, m)]

def in_degree(graph):
    deg = {k: 0 for k in graph.keys()}
    for v in graph.values():
        nodes = v.keys()
        for node in nodes:
            if node not in deg:
                deg[node] = 1
            else:
                deg[node] += 1

    return deg

def topological_ordering(graph):
    deg = in_degree(graph)
    n = len(deg.items())
    ordering = []

    x = 0
    while deg:
        a = deg.copy().items()
        i = len(a)
        
        x += 1
        if x % 10 == 0:
            print(f"{n-i} of {n}")
        
        for k, v in a:
            if v == 0:
                del deg[k]
                ordering.append(k)
                if k not in graph:
                    continue
                for nbr in graph[k].keys():
                    deg[nbr] -= 1

    return ordering

def complement_graph(graph):
    res = {}
    for k, v in graph.items():
        nbrs = v.keys()
        for nbr in nbrs:
            if nbr not in res:
                res[nbr] = [k]
            else:
                res[nbr].append(k)
    return res

def longest_path(graph):
    print("finding topological ordering")
    top_ord = topological_ordering(graph)
    print("end topological ordering")
    complement = complement_graph(graph)

    backtrack = {}
    weight = {top_ord[0]: 0}
    for node in top_ord[1:]:
        backnodes = complement[node]
        backnodes_weight = {
            backnode: weight[backnode] + graph[backnode][node]
            for backnode in backnodes
        }

        backnode = max(backnodes_weight, key=backnodes_weight.get)

        backtrack[node] = backnode
        weight[node] = backnodes_weight[backnode]


    # backtrack path
    start = top_ord[0]
    end = top_ord[-1]
    path = [end]
    next_node = end
    while True:
        next_node = backtrack[next_node]
        path.append(next_node)
        if next_node == start:
            break

    return path[::-1], weight[end]

def LCS_graph(v, w, indel=0, mismatch=0, match=1):
    m = len(v)
    n = len(w)

    graph = {k: {} for k in product(range(m+1), range(n+1))}

    for i in range(m):
        for j in range(n):
            graph[(i, j)][(i, j+1)] = -indel 
            graph[(i, j)][(i+1, j)] = -indel
            graph[(i, j)][(i+1, j+1)] = match if v[i] == w[j] else -mismatch

    for i in range(m):
        graph[(i, n)][(i+1, n)] = -indel

    for j in range(n):
        graph[(m, j)][(m, j+1)] = -indel

    return graph

def alignment(v, w, indel=0, mismatch=0, match=1):
    path, weight = longest_path(LCS_graph(v, w, match=match, mismatch=mismatch, indel=indel))

    start = path[0]
    cur_node = start
    v_res = []
    w_res = []
    common = []
    for tail in path[1:]:
        i, j = cur_node
        x = tail[0] - cur_node[0]
        y = tail[1] - cur_node[1]
        if (x, y) == (1, 1):
            v_res.append(v[i])
            w_res.append(w[j])
            if v[i] == w[j]:
                common.append(v[i])
        if (x, y) == (0, 1):
            v_res.append("-")
            w_res.append(w[j])
        if (x, y) == (1, 0):
            v_res.append(v[i])
            w_res.append("-")

        cur_node = tail

    return "".join(v_res), "".join(w_res), "".join(common), weight



if __name__ == "__main__":
    # with open("datasets/dataset_261_10.txt") as file:
    #     down = []
    #     while True:
    #         line = file.readline().strip()
    #         if line == "-":
    #             break
    #         line = list(map(int, line.split(" ")))
    #         down.append(line)
    #
    #     right = []
    #     while True:
    #         line = file.readline()
    #         if not line:
    #             break
    #         line = list(map(int, line.strip().split(" ")))
    #         right.append(line)
    #
    # grid = manhattan_tourist_graph(down, right)
    # print(manhattan_tourist(grid, 17, 10))

    # print(longest_path({
    #     0: {1: 7, 2: 4},
    #     1: {4: 1},
    #     2: {3: 2},
    #     3: {4: 3},
    # }))

    # graph = {}
    # with open("datasets/dataset_245_7.txt") as file:
    #     for line in file.readlines():
    #         line = list(map(int, line.strip().split(" ")))
    #         if line[0] not in graph:
    #             graph[line[0]] = {line[1]: line[2]}
    #         else:
    #             graph[line[0]][line[1]] = line[2]
    #
    # print(*longest_path(graph)[0])
    # print(longest_path(graph)[1])

    # with open("datasets/dataset_245_5.txt") as file:
    #     a = file.readline().strip()
    #     b = file.readline().strip()
    #     # b = "GACT"
    #     # a = "ATG"
    #     print(*alignment(a, b), sep="\n")

    #a = "GCGATC"
    #b =  "CTGACG"
    #print(*alignment(a, b), sep="\n")

    #x = [0, 0, 1, 1]

    #i = 3
    #while i < 24:
    #    i += 1
    #    x.append(x[i-2] + x[i-3])

    #print(x)

    #graph = {
    #    "a": {"b": 5, "c": 6, "d": 5},
    #    "b": {"c": 2, "f": 9},
    #    "c": {"e": 4, "f": 3, "g": 7},
    #    "d": {"e": 4, "f": 5},
    #    "e": {"g": 2},
    #    "f": {"g": 1}
    #}

    with open("datasets/dataset_247_3.txt") as file:
        match, mismatch, indel = list(map(int, file.readline().strip().split(" ")))
        a = file.readline().strip()
        b = file.readline().strip()
        
        # match, mismatch, indel = 1, 1, 2
        # a = "GAGA"
        # b = "GAT"
        print(*alignment(a, b, match=match, indel=indel, mismatch=mismatch), sep="\n")
