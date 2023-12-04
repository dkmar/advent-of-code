#!/usr/bin/env python3
import util
import sys, math
from collections import defaultdict, deque
from functools import cache

# 23:58
# 00:03

infile = sys.argv[1] if len(sys.argv)>1 else '16.in'
with open(infile, 'r') as f:
    #data = f.read().strip()
    lines = list(map(str.strip, f.readlines()))
    #grid = list(list(ln) for ln in map(str.strip, f.readlines()))

    graph = defaultdict(list)
    flow_rate = {}
    for ln in lines:
        v = ln.split(maxsplit=2)[1] # AA
        rate = util.get_ints(ln)[0]
        flow_rate[v] = rate
        for part in ln.split(', '):
            w = part.rsplit(maxsplit=1)[-1]
            graph[v].append(w)

'''
Valve RU has flow rate=0; tunnels lead to valves Y
Valve QK has flow rate=24; tunnels lead to valves 
Valve RP has flow rate=11; tunnels lead to valves 
Valve BX has flow rate=0; tunnels lead to valves Z
Valve JL has flow rate=0; tunnels lead to valves I

need graph, map valve to flow rate
each minute, either open or move.
opening means adding to step size.

if current is unopened, then explore 
(1) opening it and then visiting all neighbors
else
(1) explore all neighbors

alternatively, if you knew 


for part2, valves

the state is:
my location, elephant location, open valve set, time
'''

@cache
def dfs(u, valves, tm):
    if tm <= 0:
        return 0

    best = 0
    if u not in valves and flow_rate[u] > 0:
        # if we open and move
        value = flow_rate[u] * (tm-1)
        valves_u = set(valves)
        valves_u.add(u)
        for v in graph[u]:
            if value != 0:
                best = max(best, value + dfs(v, frozenset(valves_u), tm-2)) 

    for v in graph[u]:
        # if we just move
        best = max(best, dfs(v, valves, tm-1))

    return best

@cache
def dfs2(u, valves, tm):
    if tm <= 0:
        return dfs('AA', valves, 26)

    best = 0
    if u not in valves and flow_rate[u] > 0:
        # if we open and move
        value = flow_rate[u] * (tm-1)
        valves_u = set(valves) | {u}
        for v in graph[u]:
            if value != 0:
                best = max(best, value + dfs2(v, frozenset(valves_u), tm-2)) 

    for v in graph[u]:
        # if we just move
        best = max(best, dfs2(v, valves, tm-1))

    return best

src = 'AA'
best = dfs2(src, (), 26)

print(best)