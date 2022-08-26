import numpy as np
from week1_2.w1w2main import alignment

def last_column(v, w, match, mismatch, indel):
    mismatch = -mismatch
    indel = -indel

    m = len(v)
    n = len(w)

    # setup first column
    prev = [i * indel for i in range(m+1)]

    for j in range(1, n+1):
        next = [indel * j]

        if j == n:
            backtrack = ["right"]
        for i in range(1, m+1):
            diag_edge = prev[i-1] + (match if v[i-1] == w[j-1] else mismatch)
            right_edge = prev[i] + indel
            down_edge = next[-1] + indel

            # backtrack pointers (only for the last column tho, and only when going in reverse)
            if j == n:
                max_node = max(diag_edge, right_edge, down_edge)
                if max_node == diag_edge:
                    backtrack.append("diag")
                elif max_node == right_edge:
                    backtrack.append("right")
                elif max_node == down_edge:
                    backtrack.append("down")

            next.append(max(diag_edge, right_edge, down_edge))

        prev = next

    return prev, backtrack


def middle_edge(v, w, match, mismatch, indel, top, bottom, left, right):
    if right - left == 1:
        middle_col, backtrack = last_column(v[top:bottom], w[left:right], match, mismatch, indel)
        # max_ind = np.argmax(middle_col)
        # max_node = (top + max_ind, right)

        m = len(backtrack)

        for k in range(m-1, -1, -1):
            if backtrack[k] == "diag" or backtrack[k] == "right":
                max_node = (top + k, right)
                break

        i, j = max_node
        if backtrack[k] == "diag":
            nbr = (i-1, j-1)
        elif backtrack[k] == "right":
            nbr = (i, j-1)

        return [nbr, max_node], middle_col[-1]

    middle = (left + right) // 2

    left_column, _ = last_column(v[top:bottom], w[left:middle], match, mismatch, indel)
    right_column, backtrack = last_column(v[top:bottom][::-1], w[middle:right][::-1], match, mismatch, indel)
    right_column = right_column[::-1]
    backtrack = backtrack[::-1]


    middle_col = [a + b for a, b in zip(left_column, right_column)]
    max_ind = np.argmax(middle_col)
    max_node = (top + max_ind, middle)

    i, j = max_node
    if backtrack[max_ind] == "diag":
        nbr = (i+1, j+1)
    elif backtrack[max_ind] == "right":
        nbr = (i, j+1)
    elif backtrack[max_ind] == "down":
        nbr = (i+1, j)

    return [max_node, nbr], middle_col[max_ind]

def linear_space_alignment_path(v, w, match, mismatch, indel, top=0, bottom=None, left=0, right=None, depth=0):
    if bottom == None:
        bottom = len(v)
    if right == None:
        right = len(w)

    print("\t"*depth, top, bottom, left, right)

    # return a path from bottom to top
    if right == left:
        a = right
        return [(i, a) for i in range(top, bottom+1)]

    # return a path from left to right
    if bottom == top:
        b = bottom
        return [(b, j) for j in range(left, right+1)]

    mid_edge, score = middle_edge(v, w, match, mismatch, indel, top, bottom, left, right)
    a, b = mid_edge[0]
    c, d = mid_edge[1]

    print("\t"*depth + f"middle edge: {mid_edge}")



    left_path = linear_space_alignment_path(v, w, match, mismatch, indel, top, a, left, b, depth=depth+1)
    print("\t"*depth + f"left path: {left_path}")

    right_path = linear_space_alignment_path(v, w, match, mismatch, indel, c, bottom, d, right, depth=depth+1)
    print("\t"*depth + f"right path: {right_path}")

    if depth == 0:
        return left_path + right_path, score
    else:
        return left_path + right_path
















