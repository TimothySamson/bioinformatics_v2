def last_column(v, w, match, mismatch, indel, top, bottom, left, right, reverse=False):
    mismatch = -mismatch
    indel = -indel

    m = bottom - top
    n = right - left

    # setup first column
    prev = [i * indel for i in range(m+1)]

    col_range = range(left + 1, right + 1) if not reverse else range(right, left, -1)
    row_range = range(top + 1, bottom + 1) if not reverse else range(bottom, top, -1)

    for col_num, j in enumerate(col_range, 1):
        next = [indel * col_num]
        if reverse and col_num == n:
            backtrack = {(bottom, j+1): (bottom, j)}
        for row_num, i in enumerate(row_range, 1):
            diag_edge = prev[row_num-1] + (match if v[i-1] == w[j-1] else mismatch)
            right_edge = prev[row_num] + indel
            down_edge = next[-1] + indel

            # backtrack pointers (only for the last column tho, and only when going in reverse)
            if reverse and col_num == n:
                max_node = max(diag_edge, right_edge, down_edge)
                if max_node == diag_edge:
                    backtrack[(i, j)] = (i-1, j-1)
                elif max_node == right_edge:
                    backtrack[(i, j)] = (i, j - 1)
                elif max_node == down_edge:
                    backtrack[(i, j)] = (i-1, j)

            next.append(max(diag_edge, right_edge, down_edge))

        print(next)

        prev = next

    return prev, backtrack

def middle_edge(v, w, match, mismatch, indel, top, bottom, left, right):
    middle = (left + right) // 2

    left_column, _ = last_column(v, w, match, mismatch, indel, top, bottom, left, middle)







