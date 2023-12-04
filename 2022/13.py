#!/usr/bin/env python3
import util
import sys, math
from collections import defaultdict, deque

infile = sys.argv[1] if len(sys.argv)>1 else '13.in'
with open(infile, 'r') as f:
    data = f.read().strip()
    pairs = data.split('\n\n')
    # lines = list(map(str.strip, f.readlines()))
    #grid = list(list(ln) for ln in map(str.strip, f.readlines()))

'''
[[[[2],9,1,[2,2,4,8]],[1,8,8],9,[7,2,[7,0,1],0,[10
[[1,6,[[0,0,10,9]],[[10,6,0,2],[7,4],[2]],[[],3]],

[[10,10,10,4,[8,[8],6,[]]]]
[[],[[[8,2,6],0,4,10]],[8,[10,[10,4],[6]],2,7,[[8]
'''

score = lambda a,b: (a > b) - (a < b)
def cmp(a,b):
    if isinstance(a, int) and isinstance(b, int):
        return score(a,b)
    elif isinstance(a, int):
        return cmp([a], b)
    elif isinstance(b, int):
        return cmp(a, [b])
    else:
        for (x,y) in zip(a,b):
            match cmp(x,y):
                case 1:
                    return 1
                case -1:
                    return -1
                case default:
                    pass

        return cmp(len(a), len(b))

packets = []
count = 0
for (i,pair) in enumerate(pairs):
    a,b = pair.split('\n')
    a,b = eval(a), eval(b)
    packets.extend([a,b])
    if cmp(a,b) == -1:
        # print(pair.split('\n'))
        count += (i+1)

print(count)

# ---

div_p1 = [[2]]
div_p2 = [[6]]

idp1 = 0
idp2 = 1

for pkt in packets:
    if cmp(div_p1, pkt) == 1:
        idp1 += 1
        idp2 += 1
    elif cmp(div_p2, pkt) == 1:
        idp2 += 1

idp1 += 1
idp2 += 1
print(idp1, idp2)
print(idp1 * idp2)
