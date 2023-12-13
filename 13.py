#!/usr/bin/env python3
import lib
import sys, math, re, functools, operator, itertools, bisect
import numpy as np
from collections import defaultdict, deque, Counter
from itertools import accumulate, chain, pairwise, cycle, product, combinations
from functools import cache, reduce

# 21:00
infile = sys.argv[1] if len(sys.argv)>1 else '13.in'
f = open(infile, 'r') if infile != '-' else sys.stdin

# lines = list(map(lib.Input, f))
data = lib.Input(f.read())
#grid = lib.Grid.from_text(data)
blocks = data.split('\n\n')
patterns = [pat.splitlines() for pat in blocks]
'''
...##.#
.##.###
.##.###
...##.#
#...###
'''

def difference(s1: str, s2: str) -> int:
    return sum(int(a!=b) for a, b in zip(s1, s2))

def get_reflection_n(pattern: list[str], target_diff: int) -> int:
    line_numbers = range(len(pattern))
    for i,j in pairwise(line_numbers):
        start = i
        diff = 0
        while i >= 0 and j < len(pattern):
            diff += difference(pattern[i], pattern[j])
            if diff > 1:
                break
            i -= 1; j += 1
        else:
            if diff == target_diff:
                return start + 1

    return 0

def answer(pattern: list[str], target_diff: int):
    # horizontal reflection
    h = get_reflection_n(pattern, target_diff)
    if h:
        return 100 * h
    # vertical reflection
    v = get_reflection_n([str(row) for row in zip(*pattern)], target_diff)
    return v

part1 = part2 = 0
for pattern in patterns:
    part1 += answer(pattern, target_diff=0)
    part2 += answer(pattern, target_diff=1)

print(f'Part 1: {part1}')
print(f'Part 2: {part2}')
