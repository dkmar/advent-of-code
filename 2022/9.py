#!/usr/bin/env python3
import util
import sys, math
from collections import defaultdict, deque

infile = sys.argv[1] if len(sys.argv)>1 else '9.in'
with open(infile, 'r') as f:
    #data = f.read().strip()
    lines = list(map(str.strip, f.readlines()))
    #grid = list(list(ln) for ln in map(str.strip, f.readlines()))

'''
U 1
L 1
D 2
U 2
R 2
'''

