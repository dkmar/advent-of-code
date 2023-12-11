#!/usr/bin/env python3
import util
import sys, math, re, functools, operator, itertools, bisect
import numpy as np
from collections import defaultdict, deque, Counter
from itertools import accumulate, chain, pairwise, cycle
from functools import cache, reduce

# 17:21
infile = sys.argv[1] if len(sys.argv) > 1 else '10.in'
f = open(infile, 'r') if infile != '-' else sys.stdin

data = util.Input(f.read())
# lines = list(map(util.Input, f))
grid = list(list(ln) for ln in data.splitlines())

'''
F-|F|7LJ7F7.L-J7L-L-7L-J7.FF.F|--J.L-7--7.L-7FFFF7-F|---F--L
|-7FF|||F7J.FJL|.L7LL7F|J7.J.|.|JF-7LLJJL-JJLFJLL7F||.FFJ||.
F7|-LJF-F--LJ-FF7L|7FJJLF7FF-J-|-F.L.L7LLL7|F7JLF---.F-LJ|F-
-J|.|F7LJ..|LFJ-J7|J|J-||JF|7||..|-7F7L-7.|-LF7.F7|7.-J|LF|-
FFFJ||J.LFJJLJ7.J7|-77-L|-FL-L-F.LL|LJ|FJ-FJF||-F7F7-|FF7FF7
'''
m, n = len(grid), len(grid[0])


def nbrs(i, j, ch):
    match ch:
        case '|':
            return (i - 1, j), (i + 1, j)
        case '-':
            return (i, j - 1), (i, j + 1)
        case 'L':
            return (i - 1, j), (i, j + 1)
        case 'J':
            return (i - 1, j), (i, j - 1)
        case '7':
            return (i + 1, j), (i, j - 1)
        case 'F':
            return (i + 1, j), (i, j + 1)
        case '.':
            # return (i-1, j), (i+1, j), (i, j-1), (i, j+1)\
            return ()
        case 'S':
            # return (i-1, j), (i+1, j), (i, j-1), (i, j+1)
            return (i + 1, j), (i, j + 1)


def neighbors(i, j, ch):
    return tuple((i, j) for i, j in nbrs(i, j, ch) if 0 <= i < m and 0 <= j < n)


loc = data.drop('\n').find('S')
si, sj = loc // n, loc % n

q = deque([(si, sj)])
seen = {(si, sj)}

on_loop = set()
steps = 0
last = {}
while q:
    steps += 1
    for _ in range(len(q)):
        i, j = q.popleft()
        for nbr in neighbors(i, j, grid[i][j]):
            if nbr not in seen:
                q.append(nbr)
                seen.add(nbr)
                last = nbr, steps

        on_loop.add((i, j))

enclosed = []
for i, row in enumerate(grid):
    inside = False
    for j, ch in enumerate(row):
        if (i, j) in on_loop:
            if ch in '|LJ':
                inside = not inside
        elif inside:
            enclosed.append((i, j))
            grid[i][j] = 'I'

print('part 1: ', last)
print('part 2: ', len(enclosed))

# with open('9out.txt', 'w') as wf:
#     for row in grid:
#         s = ''.join(row).replace('$', ' ')
#         wf.write(s + '\n')
