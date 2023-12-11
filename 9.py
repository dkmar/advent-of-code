#!/usr/bin/env python3
import util
import sys, math, re, functools, operator, itertools, bisect
import numpy as np
from collections import defaultdict, deque, Counter
from itertools import accumulate, chain, pairwise, cycle
from functools import cache, reduce

# 16:45
infile = sys.argv[1] if len(sys.argv) > 1 else '9.in'
f = open(infile, 'r') if infile != '-' else sys.stdin

# data = f.read().strip()
lines = list(map(util.Input, f))
# grid = list(list(ln) for ln in map(str.strip, f))

'''
11 22 50 101 188 336 587 1005 1681 2738 4336 6677 10010 1463
21 36 67 138 289 580 1107 2039 3695 6718 12488 24067 48215 9
-3 -8 -18 -23 7 125 405 935 1805 3090 4828 6993 9463 11983 1
14 37 80 152 269 464 799 1391 2476 4556 8724 17371 35687 747
9 26 47 70 93 114 131 142 145 138 119 86 37 -30 -117 -226 -3
'''

histories = [util.get_ints(line, negatives=True) for line in lines]


def get_next(h: list[int]):
    diffs = list(b - a for a, b in pairwise(h))
    if not any(diffs):
        return h[-1]

    return h[-1] + get_next(diffs)


def get_prev(h: list[int]):
    diffs = list(b - a for a, b in pairwise(h))
    if not any(diffs):
        return h[0]

    return h[0] - get_prev(diffs)


p1 = p2 = 0
for h in histories:
    last = get_next(h)
    prev = get_prev(h)
    p1 += last
    p2 += prev

    # print(prev, h, last)

print(p1)
print(p2)
