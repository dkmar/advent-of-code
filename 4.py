#!/usr/bin/env python3
import lib
import sys, math, re, functools, operator
import numpy as np
from collections import defaultdict, deque, Counter

# 16:58 1703 1713

infile = sys.argv[1] if len(sys.argv)>1 else '4.in'
with open(infile, 'r') as f:
    #data = f.read().strip()
    lines = list(map(str.strip, f))
    #grid = list(list(ln) for ln in map(str.strip, f))

'''
Card   1: 79 93 21 74 81 76 17 89  3  5 |  5 67 87
Card   2: 83 16 24 23 59 70 14 57 74 53 | 79 82 70
Card   3: 12 77 13 14 48 55 69  4 18 81 | 69  7 94
Card   4: 32 35 57 27 15  5 16 40 36 46 | 84 47 76
Card   5:  8 72 57 36 45 96  7 13 17 14 | 46 40  8
'''
res = 0
num_matches = []
for line in lines:
    rhs = line.split(': ')[1]
    winning, nums = rhs.split('|')
    winning = set(map(int, winning.split()))
    nums = set(map(int, nums.split()))
    
    matches = winning & nums
    if matches:
        res += 2**(len(matches) - 1)
        
    num_matches.append(len(matches))

print(res)


cards = [1] * len(lines)
for i in range(len(lines)-1, -1, -1):
    matches = num_matches[i]
    if i+1 < len(cards):
        cards[i] += sum(cards[i+1:i+1+matches])

print(sum(cards))
