# This code is for cheking whether the given matrix can be transformmed into 4-cyclic graph
# Notice here, we just dig into Depth=10, which means we only check for the length of path=10

import itertools

def mutate(M, i):       # Mutation matrix (We perform the mutation process on matrix directly)
    n = len(M)
    M_ = [row[:] for row in M]
    for j in range(n):
        for k in range(n):
            if j != k and M[j][i] > 0 and M[i][k] > 0:
                M_[j][k] += M[j][i] * M[i][k]
                M_[k][j] -= M[j][i] * M[i][k]
    for j in range(n):
        M_[j][i] *= -1
        M_[i][j] *= -1
    return M_

def is_4_cyclic(M):     # 4 cycle detecter
    n = len(M)
    for (a, b, c, d) in itertools.permutations(range(n), 4):
        if M[a][b] > 0 and M[b][c] > 0 and M[c][d] > 0 and M[d][a] > 0:
            return True
    return False

def recursive_mutation_test(M, depth=0, history=[], last_mutated=-1, max_depth=10): # here we can change max_depth for further check 
    print(f"Depth: {depth}, Mutation Path: {history}")
    print("Current Matrix:")
    for row in M:
        print(row)
    print("-----")

    if depth >= max_depth:
        return False, "Reached maximum depth without finding a 4-cycle."

    if is_4_cyclic(M):
        return True, (history, M)

    for i in range(len(M)):
        if i != last_mutated:
            new_history = history + [i]
            mutated_matrix = mutate([row[:] for row in M], i)
            result, output = recursive_mutation_test(mutated_matrix, depth + 1, new_history, i, max_depth)
            if result:
                return True, output

    return False, None

# Our input Matrix.
M = [
    [0, -1, 0, 1],
    [1, 0, 1, -1],
    [0, -1, 0, -1],
    [-1, 1, 1, 0]
]

result, output = recursive_mutation_test(M)
if result:
    print("A 4-cycle was formed with the following mutation sequence and matrix:")
    print("Mutation Path:", output[0])
    print("Resulting Matrix:")
    for row in output[1]:
        print(row)
else:
    print(output)
