from week1_2.w1w2main import topological_ordering, alignment
from week3.affine_gap import affine_gap_graph, is_topological_ordering, affine_alignment
from week3.space_efficient import last_column, middle_edge
from itertools import product

if __name__ == "__main__":
    # m = len(v)
    # n = len(w)
    # graph, order = affine_gap_graph(v, w, 1, 1, 2, 1)

    # print(order)
    # print(is_topological_ordering(order, graph))

    # with open("week3/datasets/dataset_249_8.txt") as file:
    #     v = file.readline().strip()
    #     w = file.readline().strip()
    #
    #
    # print(*affine_alignment(v, w, 1, 5, 3, 1), sep="\n")
    # print(*alignment("A", "B", indel=1, mismatch=3), sep="\n")

    with open("week3/datasets/dataset_250_12.txt") as file:
        w = file.readline().strip()
        v = file.readline().strip()

        print(middle_edge(v, w, 1, 1, 5, 0, len(v), 0, len(w)))

    # w = "TTTT"
    # v = "CC"
    # print(middle_edge(v, w, 1, 5, 1, 0, len(v), 0, len(w)))

    # v = "GAT"
    # w = "GA"
    # print(last_column(v[::-1], w[::-1], 1, 1, 2))






