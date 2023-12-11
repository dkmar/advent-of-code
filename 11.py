#!/usr/bin/env python3
import util
import sys, math, re, functools, operator, itertools, bisect
import numpy as np
from collections import defaultdict, deque, Counter
from itertools import accumulate, chain, pairwise, cycle, product, combinations
from functools import cache, reduce

# 21:00
infile = sys.argv[1] if len(sys.argv)>1 else '11.in'
f = open(infile, 'r') if infile != '-' else sys.stdin

data = util.Input(f.read())
grid = util.Grid.from_text(data)
# lines = list(map(util.Input, f))

'''
...............#............................................
........#.............................................#.....
.....................................#......#...............
...............................#............................
.........................#..................................
'''

empty_cols = [j for j, col in grid.cols()
              if all(ch == '.' for ch in col)]
empty_rows = [i for i, row in grid.rows()
              if all(ch == '.' for ch in row)]
        
p1 = 0
p2 = 0
V = grid.where('#')
for (ui, uj), (vi, vj) in combinations(V, 2):
    i1, i2 = util.sort2(ui, vi)
    j1, j2 = util.sort2(uj, vj)
    
    er = sum(1 for r in empty_rows if i1 < r < i2)
    ec = sum(1 for c in empty_cols if j1 < c < j2)
    dist = (i2 - i1) + (j2 - j1)
    p1 += dist + (er + ec)
    p2 += dist - (er + ec) + (er + ec) * 1_000_000

print(f'part 1: {p1}')
print(f'part 2: {p2}')