#!/usr/bin/env python3
import util
import sys, math, re, functools, operator, itertools, bisect
import numpy as np
from collections import defaultdict, deque, Counter
from itertools import accumulate, chain, pairwise, cycle, starmap
from functools import cache, reduce

# 17:21
infile = sys.argv[1] if len(sys.argv) > 1 else '10.in'
f = open(infile, 'r') if infile != '-' else sys.stdin

data = util.Input(f.read())
# lines = list(map(util.Input, f))
grid = util.Grid.from_text(data)

'''
F-|F|7LJ7F7.L-J7L-L-7L-J7.FF.F|--J.L-7--7.L-7FFFF7-F|---F--L
|-7FF|||F7J.FJL|.L7LL7F|J7.J.|.|JF-7LLJJL-JJLFJLL7F||.FFJ||.
F7|-LJF-F--LJ-FF7L|7FJJLF7FF-J-|-F.L.L7LLL7|F7JLF---.F-LJ|F-
-J|.|F7LJ..|LFJ-J7|J|J-||JF|7||..|-7F7L-7.|-LF7.F7|7.-J|LF|-
FFFJ||J.LFJJLJ7.J7|-77-L|-FL-L-F.LL|LJ|FJ-FJF||-F7F7-|FF7FF7
'''

from util import Cardinal as C
dirs = {
    '|': C.N | C.S,
    '-': C.E | C.W,
    'L': C.N | C.E,
    'J': C.N | C.W,
    '7': C.S | C.W,
    'F': C.S | C.E,
    '.': C.NULL,
    'S': C.S | C.E  # for my input lolz
}

big_char = {
    '|': '.|. .|. .|.'.split(),
    '-': '... --- ...'.split(),
    'L': '.|. .L- ...'.split(),
    'J': '.|. -J. ...'.split(),
    '7': '... -7. .|.'.split(),
    'F': '... .F- .|.'.split(),
    '.': '... ... ...'.split(),
    'S': '... .F- .|.'.split(),  # for my input lolz
}

def neighbors(i, j, ch):
    yield from C.neighbors(i, j, grid.m, grid.n, dirs[ch])
    
# discover loop and track furthest
start = grid.find('S')
q = deque([start])
loop = {start}

steps = 0
while q:
    steps += 1
    for _ in range(len(q)):
        i, j = q.popleft()
        for nbr in neighbors(i, j, grid[i,j]):
            if nbr not in loop:
                q.append(nbr)
                loop.add(nbr)

        loop.add((i, j))

# furthest was added to queue one loop before the last (where frontier is finally exhausted).
furthest = steps - 1

# virtually remap to 3x and also remap all non-loop chars to '.'
class grid3x:
    m, n = 3 * grid.m, 3 * grid.n
    def __class_getitem__(cls, item):
        i3, j3 = item
        if (i3//3, j3//3) in loop:
            return big_char[grid[i3//3, j3//3]][i3 % 3][j3 % 3]
        else:
            return '.'
        

def get_enclosed() -> int:
    # get all 3x locations for those outside the loop.
    def outside_locs():
        i, j = next(loc for loc in grid.keys() if loc not in loop)
        seen = {(3*i, 3*j)}
        q = deque([(3*i, 3*j)])
        while q:
            i, j = q.popleft()
            # yield if this is the canonical 3x loc
            if i % 3 == 0 and j % 3 == 0:
                yield i, j

            for nbr in util.neighbors(i, j, grid3x.m, grid3x.n):
                if nbr not in seen and grid3x[nbr] == '.':
                    seen.add(nbr)
                    q.append(nbr)
    
    # determine which locations are entirely empty by checking the middle char.
    def is_empty(i, j):
        return grid3x[i+1, j+1] == '.'
    
    # count once per 3x cell representing an outside cell.
    outside = sum(1 for i,j in outside_locs() if is_empty(i, j))
    # N - those outside the loop - those on the loop = those enclosed by the loop
    return (grid.m * grid.n) - outside - len(loop)
            

print('part 1: ', furthest)
print('part 2: ', get_enclosed())

# with open('9out.txt', 'w') as wf:
#     for i in range(grid3x.m):
#         row = (grid3x[i,j] for j in range(grid3x.n))
#         s = ''.join(row).replace('.', ' ')
#         wf.write(s + '\n')
