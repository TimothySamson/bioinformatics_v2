import week1_2.exercises
from itertools import product
from pprint import pprint

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


def longest_path(graph, top_ord=None):
    if not top_ord:
        top_ord = topological_ordering(graph)
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


def LCS_graph(v, w, indel=0, mismatch=0, match=1, local=False, score=None):
    m = len(v)
    n = len(w)

    graph = {k: {} for k in product(range(m+1), range(n+1))}

    if local:
        for coord in graph.keys():
            if coord != (0, 0) and coord != (m, n):
                graph[(0, 0)][coord] = 0
                graph[coord][(m, n)] = 0

    for i in range(m):
        for j in range(n):
            graph[(i, j)][(i, j+1)] = -indel 
            graph[(i, j)][(i+1, j)] = -indel
            if not score:
                graph[(i, j)][(i+1, j+1)] = match if v[i] == w[j] else -mismatch
            else:
                graph[(i, j)][(i+1, j+1)] = score[v[i]][w[j]]

    for i in range(m):
        graph[(i, n)][(i+1, n)] = -indel

    for j in range(n):
        graph[(m, j)][(m, j+1)] = -indel

    return graph


# WEEK 2
def fitting_alignment(long, short, indel, mismatch, match, score=None):
    m = len(long)
    n = len(short)
    orig = LCS_graph(long, short, indel, mismatch, match, score=score)


    for i in range(m):
        orig[(0, 0)][(i, 0)] = 0
        orig[(i, n)][(m, n)] = 0

    top_ordering = [(i, j) for i in range(m+1) for j in range(n+1)]
    path, weight = longest_path(orig, top_ord=top_ordering)
    return *path_to_alignment(long, short, path), weight


# WEEK 2
def overlap_alignment(v, w, match=1, mismatch=1, indel=2):
    m = len(v)
    n = len(w)
    orig = LCS_graph(v, w, indel=indel, match=match, mismatch=mismatch)

    for i in range(m):
        orig[(i, 0)][(i+1, 0)] = 0

    for j in range(n):
        orig[(m, j)][(m, j+1)] = 0

    top_ordering = [(i, j) for i in range(m+1) for j in range(n+1)]
    path, weight = longest_path(orig, top_ord=top_ordering)
    return *path_to_alignment(v, w, path), weight


def path_to_alignment(v, w, path):
    tail = path[0]
    v_res = []
    w_res = []
    common = []
    for head in path[1:]:
        i, j = tail
        x = head[0] - tail[0]
        y = head[1] - tail[1]

        # GENERAL CASES
        if (x, y) == (1, 1):
            v_res.append(v[i])
            w_res.append(w[j])
            if v[i] == w[j]:
                common.append(v[i])
        elif (x, y) == (0, 1):
            v_res.append("-")
            w_res.append(w[j])
        elif (x, y) == (1, 0):
            v_res.append(v[i])
            w_res.append("-")

        tail = head

    return "".join(v_res), "".join(w_res), "".join(common)


def alignment(v, w, indel=0, mismatch=0, match=1, local=False, score=None):
    m = len(v)
    n = len(w)
    top_ordering = [(i, j) for i in range(m+1) for j in range(n+1)]
    graph = LCS_graph(v, w, match=match, mismatch=mismatch, indel=indel, local=local, score=score)
    path, weight = longest_path(graph, top_ord=top_ordering)

    # PATH TO ALIGNMENT
    start = path[0]
    tail = start
    v_res = []
    w_res = []
    common = []
    for head in path[1:]:
        i, j = tail
        x = head[0] - tail[0]
        y = head[1] - tail[1]

        # GENERAL CASES
        if (x, y) == (1, 1):
            v_res.append(v[i])
            w_res.append(w[j])
            if v[i] == w[j]:
                common.append(v[i])
        elif (x, y) == (0, 1):
            v_res.append("-")
            w_res.append(w[j])
        elif (x, y) == (1, 0):
            v_res.append(v[i])
            w_res.append("-")

        # SPECIAL CASES
        if tail in [(1, 0), (0, 1), (1, 1), (m, n)] and local:
            cur_v = v_res[-1]
            cur_w = w_res[-1]

            if cur_v == "-" or cur_w == "-":
                del v_res[-1]
                del w_res[-1]
            elif score[cur_v][cur_w] < 0:
                del v_res[-1]
                del w_res[-1]
                weight -= score[cur_v][cur_w]

        tail = head

    return "".join(v_res), "".join(w_res), "".join(common), weight

def scoring_table(filename):
    with open(filename) as file:
        keys = file.readline().strip().split()
        score = {key: {} for key in keys}
        for line, key1 in zip(file.readlines(), keys):
            line = list(map(int, line.strip().split()[1:]))
            score[key1] = {
                key2: val
                for val, key2 in zip(line, keys)
            }

    return score

def PAM250_score():
    return scoring_table("datasets/PAM250.txt")

def hamming_distance(p, q):
    if len(p) != len(q):
        raise ValueError("length of p equals length of q")

    count = 0
    n = len(p)
    for i in range(0, n):
        if p[i] != q[i]:
            count += 1

    return count


def edit_distance(v, w):
    _, _, _, score = alignment(v, w, indel=1, mismatch=1, match=0)
    return -score

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

    # with open("datasets/dataset_247_10.txt") as file:
    #     a = file.readline().strip()
    #     b = file.readline().strip()
    #
    #     print(*alignment(a, b, indel=5, local=True, score=PAM250_score()), sep="\n")
    # a = "MEANLY"
    # b = "PENALTY"
    # print(*alignment(a, b, indel=5, local=True, score=PAM250_score()), sep="\n")

    # with open("datasets/dataset_248_3.txt") as file:
    #     v = file.readline().strip()
    #     w = file.readline().strip()
    #
    #     print(edit_distance(v, w))

    # with open("datasets/dataset_248_5.txt") as file:
    #     long = file.readline().strip()
    #     short = file.readline().strip()
    #     print(*fitting_alignment(long, short), sep="\n")



    # with open("datasets/dataset_248_7.txt") as file:
    #     v = file.readline().strip()
    #     w = file.readline().strip()
    #     print(*overlap_alignment(v, w), sep="\n")

    v = "ACGACCACAGATACCGCTATTCACTATATCGTT"
    w = "GATACACT"
    print(*fitting_alignment(v, w, 1, 1, 1), sep="\n")


