import sys

sys.setrecursionlimit(2000)


def get_backtrack(v, w, scoring_matrix, indel=5):
    n = len(v)
    m = len(w)

    s = {0: {}}
    backtrack = {}
    s[0][0] = 0

    for i in range(1, n + 1):
        s[i] = dict()
        backtrack[i] = dict()
        s[i][0] = 0

    for j in range(1, m + 1):
        s[0][j] = 0

    max_score, max_i, max_j = [0]*3
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            s[i][j] = max([s[i - 1][j] - indel,
                           s[i][j - 1] - indel,
                           0])
            if v[i - 1] == w[j - 1]:
                s[i][j] = max([s[i][j], s[i - 1][j - 1] + scoring_matrix[v[i-1]][w[j-1]]])
            if v[i - 1] != w[j - 1]:
                s[i][j] = max([s[i][j], s[i - 1][j - 1] + scoring_matrix[v[i-1]][w[j-1]]])

            if s[i][j] == s[i - 1][j - 1] + scoring_matrix[v[i-1]][w[j-1]] and v[i - 1] == w[j - 1]:
                backtrack[i][j] = 'good_diag'
            elif s[i][j] == s[i - 1][j] - indel:
                backtrack[i][j] = 'down'
            elif s[i][j] == s[i][j - 1] - indel:
                backtrack[i][j] = 'right'
            elif s[i][j] == s[i - 1][j - 1] + scoring_matrix[v[i-1]][w[j-1]] and v[i - 1] != w[j - 1]:
                backtrack[i][j] = 'bad_diag'
            elif s[i][j] == 0:
                backtrack[i][j] = 'STOP'

            if s[i][j] > max_score:
                max_score, max_i, max_j = s[i][j], i, j

    i = max_i
    j = max_j
    v_aligned, w_aligned = v[:i], w[:j]
    while i != 0 and j != 0 and backtrack[i][j] != 'STOP':
        if backtrack[i][j] == 'down':
            i -= 1
            w_aligned = w_aligned[:j] + '-' + w_aligned[j:]
        elif backtrack[i][j] == 'right':
            j -= 1
            v_aligned = v_aligned[:i] + '-' + v_aligned[i:]
        else:
            i -= 1
            j -= 1

    v_aligned = v_aligned[i:]
    w_aligned = w_aligned[j:]

    return max_score, v_aligned, w_aligned


if __name__ == '__main__':
    scoring_matrix = {}
    with open('PAM250.txt') as input_data:
        for line in input_data.readlines():
            letter_from, letter_to, cost = line.strip().split()
            cost = int(cost)
            if letter_from not in scoring_matrix:
                scoring_matrix[letter_from] = {}
            scoring_matrix[letter_from][letter_to] = cost

    with open('in.txt', 'r') as f:
        v = f.readline().strip()
        w = f.readline().strip()
    score, v, w = get_backtrack(v, w, scoring_matrix)
    print (score)
    print (v)
    print (w)
    # path = list(map(str, path))
    # with open('out.txt', 'w') as f:
    #     f.write('\n'.join([str(max_cost), '->'.join(path)]))
