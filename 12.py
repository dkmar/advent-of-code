#!/usr/bin/env python3
from networkx.algorithms.centrality import group

import lib
import sys, math, re, functools, operator, itertools, bisect
import numpy as np
from collections import defaultdict, deque, Counter
from itertools import accumulate, chain, pairwise, cycle, product, combinations, groupby, repeat
from more_itertools import sliding_window
from functools import cache, reduce

# 14:53
infile = sys.argv[1] if len(sys.argv) > 1 else '12.in'
f = open(infile, 'r') if infile != '-' else sys.stdin

lines = list(map(lib.Input, f))
# data = lib.Input(f.read())
# grid = lib.Grid.from_text(data)

'''
??.?#??#?#??##???? 2,4,6,1
?????#?..?#? 2,2,2
???#???#.?#?????.# 5,1,1,1,2,1
???#???#.#??#??##?? 1,1,1,1,9
????###??.????#.# 5,1,2,1

? = .|#
want: the sum of possible configs across all given (springs, broken)

????.#####??.#####. 1,6,5
???? #####??  1,6
cases:
1. we meet the first broken
2. we don't and we leave it for the next group
??#? #####??  3,6
need = broken[0] - group.count(#) 

??#? 1,2
?? # ?

??#??? 3 2
'''


@cache
def waysV2(springs: str, broken: tuple[int, ...], group_size: int = 0) -> int:
    if not springs:
        return (not broken and group_size == 0)
    if not broken:
        return ('#' not in springs)

    ways = 0
    if springs[0] in '#?':
        ways += waysV2(springs[1:], broken, group_size + 1)
    if springs[0] in '.?':
        # starting a group or terminating a group
        if group_size == 0:
            ways += waysV2(springs[1:], broken, 0)
        elif group_size == broken[0]:
            ways += waysV2(springs[1:], broken[1:], 0)

    return ways


@cache
def waysV3(springs: str, broken: tuple[int, ...]) -> int:
    if not broken:
        return int('#' not in springs)
    if not springs:
        return 0

    ways = 0
    need = broken[0]
    if springs[0] in '#?' and len(springs) > need:
        # if we terminate with a good char (for separation) and this window is all #: count
        if (springs[need] in '.?') and not lib.drop(springs[:need], '#?'):
            ways += waysV3(springs[need + 1:], broken[1:])
    if springs[0] in '.?':
        ways += waysV3(springs[1:], broken)

    return ways


@cache
def countWays(springs: str, broken: tuple[int, ...]) -> int:
    '''
    Match the first broken group.
    ??#?.######..#####. 2,6,5
    '''
    if not broken:
        return int('#' not in springs)

    need = broken[0]
    ways = 0
    # window must use the first broken streak if there is one.
    first_broken = i if (i := springs.find('#')) != -1 else len(springs)
    for i, window in enumerate(sliding_window(springs, need + 1)):
        if i > first_broken:
            break
        if (window[-1] in '.?') and all(ch in '#?' for ch in window[:need]):
            ways += countWays(springs[i + need + 1:], broken[1:])

    return ways


part1 = part2 = 0
for line in lines:
    springs, broken = line.split()
    broken = tuple(lib.get_ints(broken))
    part1 += waysV3(springs + '.', broken)

    springs = '?'.join(repeat(springs, 5)) + '.'
    broken = broken * 5
    part2 += waysV3(springs, broken)

print('Part 1:', part1)
print('Part 2:', part2)
print(waysV3.cache_info())
