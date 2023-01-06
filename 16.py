#!/usr/bin/env python3
from typing import FrozenSet
import util
import sys, math
from collections import defaultdict, deque

# 18:13

infile = sys.argv[1] if len(sys.argv)>1 else '16.in'
with open(infile, 'r') as f:
    #data = f.read().strip()
    lines = list(map(str.strip, f.readlines()))
    flow_rate = {}
    graph = {}

    for fields in map(str.split, lines):
        src = fields[1]
        rate = util.get_ints(fields[4])[0]
        dsts = [dst.rstrip(',') for dst in fields[9:]]

        flow_rate[src] = rate
        graph[src] = dsts

'''
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
'''

cnt = [0]
sys.setrecursionlimit(1_000)
def max_flow(u: str, opened_valves: FrozenSet[str], time: int = 30) -> int:
    cnt[0] += 1
    '''
    Return the max possible flow from the path starting at u.
    '''
    if time <= 0:
        return 0

    # case 1: we don't open this valve.
    best = max(max_flow(v, opened_valves, time - 1) for v in graph[u])

    # case 2: we open this valve, then transition.
    if u in opened_valves or flow_rate[u] == 0:
        # early exit if it doesn't make sense to open the valve
        return best
    score = flow_rate[u] * (time - 1)
    opened_valves = opened_valves | {u}
    best = score + max(max_flow(v, opened_valves, time - 2) for v in graph[u])

    return best

best = max_flow('AA', frozenset(), 15)
print(best, f'calls = {cnt[0]}')
