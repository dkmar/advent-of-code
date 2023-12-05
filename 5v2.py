#!/usr/bin/env python3
import util
import sys, math, re, functools, operator, itertools, bisect
import numpy as np
from collections import defaultdict, deque, Counter
import portion as P

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

lookup: dict[str, str] = {}
maps: dict[str, P.IntervalDict] = {}
for part in parts[1:]:
    lines = part.splitlines()
    title = lines[0].split(' map:')[0]
    x = title.split('-')
    src, dst = x[0], x[2]
    lookup[src] = dst

    range_mappings = P.IntervalDict()
    for line in lines[1:]:
        dst_start, src_start, n = [int(v) for v in line.split(' ')]
        src_end = src_start + n
        
        # start, end : diff
        range_mappings[P.closedopen(src_start, src_end)] = dst_start - src_start

    maps[dst] = range_mappings


def get_location(src: str, loc: int) -> int:
    if src == 'location':
        return loc
    
    dst = lookup[src]
    dst_subranges_map = maps[dst]
    diff = dst_subranges_map.get(loc, default=0)

    return get_location(dst, loc + diff)

locs = (get_location('seed', seed) for seed in seeds)
min_loc = min(locs)
print('part 1: ', min_loc)

# -------------------------------------------------------
seeds2 = util.batched(seeds, 2)

def next_ranges(dst: str, ranges: list[tuple[int, int]]):
    '''
    range = (src_start, src_end)
    for each src range, get its subranges in dst
    '''
    dst_range_map = maps[dst]
    for start, end in ranges:
        src_range = P.closedopen(start, end)
        subranges = []
        dst_subranges_map = dst_range_map.get(src_range, default=0)
        for dst_range, diff in dst_subranges_map.items():
            subranges.append((dst_range.lower + diff, dst_range.upper + diff))

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
