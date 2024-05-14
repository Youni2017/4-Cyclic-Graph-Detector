# This code is for cheking whether the random matrix can be transformmed into 4-cyclic graph
# Notice here, we just dig into Depth=10, which means we only check for the length of path=10
# We set an iteration as well, to adjust the weights of adjacent matrix 
# We output two cases: successful cases & failed cases
# But here, I'd suggest that matain weight<10 here, since we want to output two cases, otherwise, the code will break dowm

import itertools
import random
from collections import deque

def generate_matrices_in_order():
    # Generate matrices using ordered combinations/ set range (-2,3) to test weight [-2,2] for example
    # If we want to change the edge weight into [-5,5], change the code into range(-5,6) here
    for a, b, c, d, e, f in itertools.product(range(-2, 3), repeat=6):
        M = [
            [0,  a,  b,  c],
            [-a, 0,  d,  e],
            [-b, -d, 0,  f],
            [-c, -e, -f, 0]
        ]
        if check_strong_connectivity(M):
            yield M

def check_strong_connectivity(M):
    # Use DFS to check strong connectivity
    def dfs(current, visited):
        visited.add(current)
        for i in range(4):
            if M[current][i] != 0 and i not in visited:
                dfs(i, visited)
    
    # Check if all nodes are reachable from each node
    for i in range(4):
        visited = set()
        dfs(i, visited)
        if len(visited) != 4:
            return False
    return True

def mutate(M, i):
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

def is_4_cyclic(M):
    n = len(M)
    for (a, b, c, d) in itertools.permutations(range(n), 4):
        if M[a][b] > 0 and M[b][c] > 0 and M[c][d] > 0 and M[d][a] > 0:
            return True
    return False

def search_matrices(M, strategy='BFS', max_depth=10):
    queue = deque([(M, [])]) if strategy == 'BFS' else [(M, [])]
    while queue:
        current_M, path = (queue.popleft() if strategy == 'BFS' else queue.pop())
        if len(path) >= max_depth:
            continue
        for i in range(len(current_M)):
            new_M = mutate([row[:] for row in current_M], i)
            new_path = path + [i]
            if is_4_cyclic(new_M):
                return True, new_path, new_M
            queue.append((new_M, new_path))
    return False, None, None 

def test_matrices():
    count = 0
    non_cyclic_matrices = []
    for M in generate_matrices_in_order():
        count += 1
        print(f"Testing matrix #{count}:")
        for row in M:
            print(row)
        
        result, path, final_matrix = search_matrices(M, strategy='BFS')
        if not result:
            non_cyclic_matrices.append(M)

        result, path, final_matrix = search_matrices(M, strategy='DFS')
        if not result:
            non_cyclic_matrices.append(M)

    if non_cyclic_matrices:
        print("Matrices that did not form a 4-cycle:")
        for matrix in non_cyclic_matrices:
            for row in matrix:
                print(row)
            print()  

test_matrices()