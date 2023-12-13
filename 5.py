#!/usr/bin/env python3
import lib
import sys, math, re, functools, operator, itertools, bisect
import numpy as np
from collections import defaultdict, deque, Counter

# 21:00 2136

infile = sys.argv[1] if len(sys.argv) > 1 else '5.in'
f = open(infile, 'r') if infile != '-' else sys.stdin

data = f.read().strip()
# lines = list(map(str.strip, f))
parts = data.split('\n\n')
# grid = list(list(ln) for ln in map(str.strip, f))

'''
seeds: 1514493331 295250933 3793791524 105394212 828589016 6

seed-to-soil map:
3352941879 1247490906 129850502
1738919961 2189748071 56658550
dst_start src_start n

map of map names to the maps themselves
have ranges (start, end, diff)

[           ]
[  ] [] [ ]
 [    ] []
'''

seeds = parts[0].split(': ')[1].split()
seeds = [int(seed) for seed in seeds]

lookup = {}
maps = {}
for part in parts[1:]:
    lines = part.splitlines()
    title = lines[0].split(' map:')[0]
    x = title.split('-')
    src, dst = x[0], x[2]
    lookup[src] = dst

    start_ends = []
    for line in lines[1:]:
        dst_start, src_start, n = [int(v) for v in line.split(' ')]
        src_end = src_start + n
        
        # start, end, diff
        start_ends.append((src_start, src_end, dst_start - src_start))

    start_ends.sort()
    maps[dst] = start_ends


def get_location(seed):
    src = 'seed'
    loc = seed
    while src != 'location':
        dst = lookup[src]
        for start, end, diff in maps[dst]:
            if start <= loc < end:
                loc += diff
                break

        src = dst

    return loc


min_loc = min(map(get_location, seeds))
print('part 1: ', min_loc)

# -------------------------------------------------------
seeds2 = lib.batched(seeds, 2)

def next_ranges(dst: str, ranges: list[tuple[int, int]]):
    '''
    range = (src_start, src_end)
    for each src range, get its subranges in dst
    '''
    for start, end in ranges:
        subranges = []
        for src_start, src_end, diff in maps[dst]:
            # case: non-overlapping
            if end <= src_start:
                #    [   ]     
                #         [  ] [] ...
                break
            elif src_end <= start:
                #    [   ]     
                #  [] [  ]? ...       
                continue

            # case: some overlap
            sub_start = max(start, src_start)
            sub_end = min(end, src_end)

            # non-overlapping prefix
            if start < sub_start:
                # [  ]
                #   [  ]
                excluded = (start, sub_start)
                subranges.append(excluded)

            # overlap
            subranges.append((sub_start + diff, sub_end + diff))

            # update suffix yet to be covered
            start = sub_end
            # break if covering
            if start == end:
                break

        # cover any non-overlapping suffix that remains 
        if start < end:
            excluded = (start, end)
            subranges.append(excluded)

        yield subranges


def get_min_loc(src: str, src_ranges: list[tuple[int, int]]):
    if src == 'location':
        return min(start for start, end in src_ranges)

    dst = lookup[src]
    all_dst_ranges = next_ranges(dst, src_ranges)
    return min(get_min_loc(dst, dst_ranges) for dst_ranges in all_dst_ranges)


src_ranges = [(seed, seed + n) for seed, n in seeds2]
min_loc = get_min_loc('seed', src_ranges)
print('part 2: ', min_loc)
