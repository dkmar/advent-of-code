#!/usr/bin/env python3
import util
import sys, math
from collections import defaultdict, deque

# 20:37

infile = sys.argv[1] if len(sys.argv)>1 else '15.in'
with open(infile, 'r') as f:
    #data = f.read().strip()
    lines = list(map(str.strip, f.readlines()))
    #grid = list(list(ln) for ln in map(str.strip, f.readlines()))

'''
Sensor at x=155404, y=2736782: closest beacon is a
Sensor at x=2209843, y=541855: closest beacon is a
Sensor at x=3437506, y=3046523: closest beacon is 
Sensor at x=925392, y=1508378: closest beacon is a
Sensor at x=2349988, y=3272812: closest beacon is 
'''

row = 2_000_000

def manhat(sx,sy,bx,by) -> int:
    return abs(by-sy) + abs(bx-sx)

leftmost, rightmost = sys.maxsize, 0
beacons = set()
sensors = set()
for line in lines:
    (sx,sy,bx,by) = util.get_ints(line)
    dist = manhat(sx,sy,bx,by)

    d = dist - abs(row - sy)
    if d >= 0:
        sensors.add((sx,sy,dist))
        beacons.add((bx,by))

        leftmost = min(leftmost, sx-d)
        rightmost = max(rightmost, sx+d)

'''
a beacon cannot be present in radius [0, closest_beacon) 

for every cell in row n,
    look at whether a sensor's radius disqualifies the cell.

map sensor (x,y) to radius
'''

count = 0
for j in range(leftmost, rightmost+1):
    if (j,row) in beacons:
        continue

    for (x,y, r) in sensors:
        d = manhat(j,row, x,y)
        if d <= r:
            count += 1
            break

print(count)