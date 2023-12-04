#!/usr/bin/env python3
import sys
from collections import defaultdict
infile = sys.argv[1] if len(sys.argv)>1 else '12.in'
with open(infile, 'r') as f:
    #data = f.read().strip()
    grid = list(list(ln) for ln in map(str.strip, f.readlines()))

'''
abccccccccaaaaccccaaacaccccaaaaaacccccccccccaaaccc
abccccccccaaaaccaaaaaaaacccaaaaaacccccccccccaaaacc
abcccccccccaacccaaaaaaaaccccaaaaacccccccccccaaaacc
'''
m,n = len(grid),len(grid[0])
S = next((i,j) for i in range(m) for j in range(n) if grid[i][j] == 'S')
grid[S[0]][S[1]] = 'a'

import math
from util import neighbors
from collections import deque

def bfs(i,j) -> int:
    q = deque()
    q.append((0, i, j)) # dist, i,j
    visited = [[False]*n for _ in range(m)] 
    visited[S[0]][S[1]] = True
    while q:
        dist, i, j = q.popleft()
        # print(dist,grid[i][j])
        h = ord(grid[i][j])

        for (ni,nj) in neighbors(i,j, m,n):
            if not visited[ni][nj]:
                if grid[ni][nj] == 'E':
                    if ord('z') <= h+1:
                        return dist+1
                elif ord(grid[ni][nj]) <= h+1:
                    visited[ni][nj] = True
                    q.append((dist+1, ni, nj))

    return sys.maxsize

res = math.inf
for i in range(m):
    for j in range(n):
        if grid[i][j] == 'a':
            res = min(res, bfs(i,j))

print(res)