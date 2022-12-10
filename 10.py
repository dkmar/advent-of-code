#!/usr/bin/env python3
import sys
from collections import defaultdict
infile = sys.argv[1] if len(sys.argv)>1 else '10.in'
with open(infile, 'r') as f:
    #data = f.read().strip()
    lines = list(map(str.strip, f.readlines()))

'''
addx 1
addx 4
addx 1
'''

x = 1
cycle = 1
aligned = lambda: abs((cycle-1)%40 - x) <= 1
out = []

for line in lines:
    out.append('#' if aligned() else ' ')
    cycle += 1
    match line.split():
        case 'addx', n:
            out.append('#' if aligned() else ' ')
            cycle += 1
            x += int(n)

for i in range(0, len(out), 40):
    print(''.join(out[i:i+40]))