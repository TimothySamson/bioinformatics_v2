from week1_2.w1w2main import topological_ordering, alignment
from week3.affine_gap import affine_gap_graph, is_topological_ordering, affine_alignment
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
    print(*alignment("A", "B", indel=1, mismatch=3), sep="\n")
