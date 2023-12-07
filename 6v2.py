#!/usr/bin/env python3
import util
import sys, math, re, functools, operator, itertools, bisect
import numpy as np
from collections import defaultdict, deque, Counter

# 14:05

infile = sys.argv[1] if len(sys.argv) > 1 else '6.in'
f = open(infile, 'r') if infile != '-' else sys.stdin

# data = f.read().strip()
lines = list(map(str.strip, f))
# grid = list(list(ln) for ln in map(str.strip, f))

'''
Time:        40     70     98     79
Distance:   215   1051   2147   1005
---
ms, mm
speed = 1mm/ms held

dist = (time - held) * held
     = time*held - held^2
held^2 - time*held + dist = 0

charge to move
can only charge at the beginning

find # ways we can win each race
then return product of these # ways
'''

times = util.get_ints(lines[0])
record_dists = util.get_ints(lines[1])


def ways_to_win(time, record_dist):
    # ax^2 + bx + c = 0 
    # held^2 - time*held + dist = 0
    d = math.sqrt(time*time - 4*record_dist)
    if d == 0:
        # only meet record dist one time, can't pass it.
        return 0
    else:
        # first time we pass record dist
        start = int((time - d) / 2 + 1)
        # second time we pass record dist
        end = math.ceil((time + d) / 2)
        
        return end - start
    

ways = map(ways_to_win, times, record_dists)
part1 = functools.reduce(operator.mul, ways)
print('part 1: ', part1)

times = int(''.join(map(str, times)))
record_dists = int(''.join(map(str, record_dists)))
part2 = ways_to_win(times, record_dists)
print('part 2: ', part2)
