#!/usr/bin/env python3
from lib import *

# 21:00
infile = sys.argv[1] if len(sys.argv) > 1 else '15.in'
f = open(infile, 'r') if infile != '-' else sys.stdin

lines = list(map(Input, f))
# data = Input(f.read())
# grid = Grid.from_text(data)

'''
rr=8,dd-,qck-,hkk=8,xfmqn=4,sx-,mgm=4,rkbh=8,scdp-,jllv=6,vg
'''

def step_hash(step: str):
    h = 0
    for ch in step:
        h += ord(ch)
        h *= 17
        h %= 256
    return h

steps = lines[0].split(',')
part1 = sum(map(step_hash, steps))
part2 = 0

boxes = defaultdict(dict)
for step in map(Input, steps):
    # label-
    # label=focal_len
    match step.partition_any('-='):
        case (lbl, '-', _):
            boxes[step_hash(lbl)].pop(lbl, None)
        case (lbl, '=', fl):
            boxes[step_hash(lbl)][lbl] = int(fl)

for (box_id, box) in boxes.items():
    for lens, focal_len in enumerate(box.values(), 1):
        part2 += (box_id + 1) * lens * focal_len

print(f'Part 1: {part1}')
print(f'Part 2: {part2}')
