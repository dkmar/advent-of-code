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
    lines = [util.get_ints(ln, negatives=True) for ln in lines]

'''
Sensor at x=155404, y=2736782: closest beacon is a
Sensor at x=2209843, y=541855: closest beacon is a
Sensor at x=3437506, y=3046523: closest beacon is 
Sensor at x=925392, y=1508378: closest beacon is a
Sensor at x=2349988, y=3272812: closest beacon is 
'''
def manhat(sx,sy,bx,by) -> int:
    return abs(by-sy) + abs(bx-sx)

M = 4_000_000
beacons = set()
sensors = set()
for line in lines:
    (sx,sy,bx,by) = line
    dist = manhat(sx,sy,bx,by)

    sensors.add((sx,sy,dist))
    beacons.add((bx,by))

'''
the distress beacon must be neighboring a beacon's perimeter.
if it is 2 cells away from some beacon perimeter, then there would have
to be another beacon's perimeter disqualifying the cell in between. Aka it's
only possible to be more than one cell away from some perimeter if you're just one
cell away from another. The distress beacon must be 1 cell away from some perimeter.

for the diamond perimeter we have
    dx = [0, dist+1]
    dy = [dist+1, 0]
'''

for (sx,sy,dist) in sensors:
    eligible_dist = dist+1
    for dx in range(eligible_dist+1):
        dy = eligible_dist - dx
        for (dx,dy) in [(dx,dy),(-dx,dy),(-dx,-dy),(dx,-dy)]:
            x, y = sx+dx, sy+dy
            if 0<=x<=M and 0<=y<=M and all(manhat(x,y, sx,sy) > d for (sx,sy,d) in sensors):
                freq = x * 4_000_000 + y
                print(freq)
                exit(0)

