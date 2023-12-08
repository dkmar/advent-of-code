#!/usr/bin/env python3
import util
import sys, math, re, functools, operator, itertools, bisect
import numpy as np
from collections import defaultdict, deque, Counter
from itertools import accumulate, chain, pairwise, cycle
from functools import cache, reduce


# 21:00
infile = sys.argv[1] if len(sys.argv) > 1 else '8.in'
f = open(infile, 'r') if infile != '-' else sys.stdin

# data = f.read().strip()
# lines = list(map(str.strip, f))
lines = list(map(util.Input, f))
# grid = list(list(ln) for ln in map(str.strip, f))

'''
LRRRLLRLLRRLRLRRRLRLRRRLRRLLRRRLRRLRLLRLLRRLRLLLLRRLRRLRLLRR

RTF = (TRM, KNP)
FNJ = (DRR, MJH)
KNM = (CGF, LSP)
'''

inst = lines[0].tr('LR', '01')
conn: dict[str, tuple[str, str]] = {}
for line in lines[2:]:
    src, l, r = line.drop('=(,)').split()
    conn[src] = (l, r)


def a_to_z() -> int:
    curr = 'AAA'
    for step, d in enumerate(cycle(map(int, inst)), 1):
        curr = conn[curr][d]
        if curr == 'ZZZ':
            return step


def z_interval(src: str) -> int:
    curr = src
    dist_to = {}
    for step, d in enumerate(cycle(map(int, inst)), 1):
        curr = conn[curr][d]
        if curr.endswith('Z'):
            if curr in dist_to:
                return step - dist_to[curr]
            dist_to[curr] = step
  

print('part 1: ', a_to_z())
srcs = (curr for curr in conn if curr.endswith('A'))
loops = map(z_interval, srcs)
all_z = reduce(math.lcm, loops)
print('part 2: ', all_z)
