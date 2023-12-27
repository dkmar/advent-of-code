#!/usr/bin/env python3
from lib import *

# 21:00
infile = sys.argv[1] if len(sys.argv)>1 else '22.in'
f = open(infile, 'r') if infile != '-' else sys.stdin

lines = list(map(Input, f))
part1 = part2 = 0
'''
1,3,231~3,3,231
4,5,264~4,5,265
7,8,70~7,9,70
6,7,173~6,9,173
1,7,106~3,7,106
'''
@dataclasses.dataclass
class Range3D:
    x: P.Interval
    y: P.Interval
    z: P.Interval

def process_input():
    xs = []
    ys = []
    bricks = []

    for bid, line in enumerate(lines):
        s, e = line.split('~')
        s = Point3D(*map(int, s.split(',')))
        e = Point3D(*map(int, e.split(',')))

        brick = Range3D(
            P.closed(s.x, e.x),
            P.closed(s.y, e.y),
            P.closed(s.z, e.z)
        )
        xs.append({brick.x: {bid}})
        ys.append({brick.y: {bid}})
        bricks.append(brick)

    return bricks, IntervalMultiDict(xs, set.union), IntervalMultiDict(ys, set.union)

def find_support(brick_id, below: list) -> set | None:
    # simulate gravity and find any supporting layer of bricks.
    brick = bricks[brick_id]
    x_overlap = set.union(*atX[brick.x].values())
    y_overlap = set.union(*atY[brick.y].values())
    xy_overlap = x_overlap & y_overlap

    # those below us which we overlap in xy with.
    eligible = xy_overlap.intersection(below)
    if not eligible:
        # nothing below us but ground. update z to the ground.
        brick.z = P.closed(1,1)
        return None
    # otherwise, we will be supported by the tallest eligible brick(s).
    maxz = max(bricks[bb].z.upper for bb in eligible)
    brick.z = P.closed(maxz+1, maxz+1 + (brick.z.upper - brick.z.lower))
    return {bb for bb in eligible if bricks[bb].z.upper == maxz}


bricks, atX, atY = process_input()
N = len(bricks)

foundation_for = defaultdict(set)
supported_by = defaultdict(list)
below = []
for brick_id in sorted(range(N), key=lambda i: bricks[i].z.lower):
    if support := find_support(brick_id, below):
        foundation_for[brick_id] = support
        for sid in support:
            supported_by[sid].append(brick_id)

    below.append(brick_id)

critical_bricks = {
    next(iter(supporters))
    for supporters in foundation_for.values() if len(supporters) == 1
}
part1 = len(bricks) - len(critical_bricks)

def count_total_supported(target_brick: int) -> int:
    eliminated = {target_brick}
    todo = [target_brick]
    while todo:
        brick_id = todo.pop()
        supported_by_me = supported_by.get(brick_id)
        if supported_by_me is None:
            continue

        for supported_brick in supported_by_me:
            if foundation_for[supported_brick] <= eliminated:
                eliminated.add(supported_brick)
                todo.append(supported_brick)


    # don't count the target_brick as fallen
    return len(eliminated) - 1


for cb in critical_bricks:
    part2 += count_total_supported(cb)

print(f'Part 1: {part1}')
print(f'Part 2: {part2}')
