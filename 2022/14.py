#!/usr/bin/env python3
import util
import sys, math
from collections import defaultdict, deque

infile = sys.argv[1] if len(sys.argv)>1 else '14.in'
with open(infile, 'r') as f:
    #data = f.read().strip()
    lines = list(map(str.strip, f.readlines()))
    #grid = list(list(ln) for ln in map(str.strip, f.readlines()))
# 7:18
'''
506,104 -> 511,104
504,96 -> 509,96
487,80 -> 487,75 -> 487,80 -> 489,80 -> 489,72 -> 
500,93 -> 500,83 -> 500,93 -> 502,93 -> 502,90 -> 
499,35 -> 504,35
'''

# read 7:24

'''
draw rocks
simulate falling
find how much sand comes to rest before flowing out of the array
'''
src = (500,0)
bound = 1000
grid = [['.']*1000 for _ in range(1000)]

def draw(p1,p2):
    if p1[0] > p2[0] or p1[1] > p2[1]:
        draw(p2,p1)
        return

    if p1[0] == p2[0]:
        x = p1[0]
        for i in range(p1[1], p2[1]+1):
            grid[i][x] = '#'
    elif p1[1] == p2[1]:
        y = p1[1]
        for j in range(p1[0], p2[0]+1):
            grid[y][j] = '#'

for line in lines:
    coords = line.split(' -> ')
    start = coords.pop(0).split(',')
    _x,_y = int(start[0]), int(start[1])
    for xy in coords:
        xy = xy.split(',')
        x,y = int(xy[0]), int(xy[1])
        draw((_x,_y), (x,y))
        _x,_y = x,y

## print
# for i in range(12):
#     for j in range(494, 505):
#         print(grid[i][j], end='')
#     print()

# drawing done 749

def drop(x,y) -> bool:
    '''
    go until stopped. 
    if left available, drop there
    elif right available, drop there.
    else place above.
    '''
    i = y
    while 0<=i<bound and 0<=x<bound and grid[i][x] == '.':
        i += 1

    if not (0<=i<bound and 0<=x<bound):
        return True
    
    if x == 0:
        # would fall off left
        return True
    elif grid[i][x-1] == '.':
        return drop(x-1,i)
    elif x == bound-1:
        # would fall off right
        return True
    elif grid[i][x+1] == '.':
        return drop(x+1,i)
    else:
        grid[i-1][x] = 'o'
        return False

count = 0
while not drop(*src):
    count += 1

print(count)
# done with p1 at 807


