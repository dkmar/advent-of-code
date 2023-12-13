#!/usr/bin/env python3
import bisect

import lib
import sys, math, re, functools, operator, itertools
import numpy as np
from collections import defaultdict, deque, Counter

# 16:00 16:35

infile = sys.argv[1] if len(sys.argv)>1 else '3.in'
with open(infile, 'r') as f:
    #data = f.read().strip()
    lines = grid = list(map(str.strip, f))
    #grid = list(list(ln) for ln in map(str.strip, f))

'''
.........798...145.........629....579.....455.....
............*.....*...........*...&...179.*.......
........459..489.817........880.........*..996....
...........@.........................813..........
...100...................*...............131......

we can extract the numbers and their start, end positions
- put the start,end in an array for bisecting
for each symbol, we can include their adjacent numbers
'''

pattern = re.compile(r'\d+')
numbers = []
start_ends = []

for line in lines:
    row = []
    for m in pattern.finditer(line):
        num = m.group(0)
        num_id = len(numbers)
        numbers.append(int(num))
        row += (m.start(0), num_id), (m.end(0)-1, num_id)
    
    start_ends.append(row)

def part1():
    good = set()
    for i, line in enumerate(lines):
        for j, ch in enumerate(line):
            if ch == '.' or ch.isdigit():
                continue
    
            for ni, nj in lib.neighbors8(i, j, len(lines), len(line)):
                if grid[ni][nj].isdigit():
                    ind = bisect.bisect_left(start_ends[ni], (nj, 0))
                    good.add(start_ends[ni][ind][1])
    
    res = sum(numbers[num_id] for num_id in good)
    print('part1: ', res)
    
def part2():
    res = 0
    for i, line in enumerate(lines):
        for j, ch in enumerate(line):
            if ch != '*':
                continue
            
            new_good = set()
            for ni, nj in lib.neighbors8(i, j, len(lines), len(line)):
                if grid[ni][nj].isdigit():
                    ind = bisect.bisect_left(start_ends[ni], (nj, 0))
                    new_good.add(start_ends[ni][ind][1])
                    
            if len(new_good) == 2:
                res += numbers[new_good.pop()] * numbers[new_good.pop()]
                 
    print('part2: ', res)

part1()
part2()
