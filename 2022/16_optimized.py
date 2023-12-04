#!/usr/bin/env python3
'''
based on 16.py except this one uses a heuristic to prune
the search space. 

we overestimate an upperbound on a path by assuming we can
open the best valves in each minute. If this upperbound falls short
of the best score already seen, then there's no way this path is worth
exploring.
'''
import util
import sys, math
from collections import defaultdict
from itertools import combinations

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

def find_distances():
    # initializing
    eta = { 
            u: { v: sys.maxsize for v in graph } 
            for u in graph 
          }

    for u,vs in graph.items():
        eta[u][u] = 0
        for v in vs:
            eta[u][v] = 1

    # floyd warshall
    for v in graph:
        for u in graph:
            for w in graph:
                uv, vw, uw = eta[u][v], eta[v][w], eta[u][w]
                if uv + vw < uw:
                    eta[u][w] = uv + vw

    return eta

best_path = 0
def possible_paths(u, valves, time, path):
    global best_path

    # prune if this path is definitely not worth exploring.
    if score_upperbound(path, time, valves) <= best_path:
        return

    for v in valves:
        new_time = time - (eta[u][v] + 1)
        if 0 < new_time < 3:
            p = path + ((new_time, v),)
            best_path = max(best_path, score(p))
            yield p
        elif new_time >= 3:
            yield from possible_paths(v, valves - {v}, new_time, path + ((new_time, v),))

    best_path = max(best_path, score(path))
    yield path

def score_upperbound(path, time, valves):
    open_order = sorted(valves, key=flow_rate.__getitem__, reverse=True)
    time_seq = range(time-1, 0, -1)
    future_path = path + tuple(zip(time_seq, open_order))

    elephant_time_seq = range(26-1, 0, -1)
    elephant_path = tuple(zip(elephant_time_seq, open_order[len(time_seq):]))
    
    return score(future_path) + score(elephant_path)

def score(path):
    res = 0
    for (time, valve) in path:
        res += time * flow_rate[valve]
    return res

eta = find_distances()
valves = frozenset(u for u in graph if flow_rate[u] != 0)

# part 1
paths = possible_paths('AA', valves, 30, ())
best = max(map(score, paths))
print(best)

# part 2
def max_scores(paths):
    '''
    find the max score for each set of valves.
    '''
    scores = defaultdict(int)
    for path in paths:
        opened_valves = frozenset(valve for (_, valve) in path)
        scores[opened_valves] = max(scores[opened_valves], score(path))

    return scores

paths = possible_paths('AA', valves, 26, ())
valveset_score = max_scores(paths)

# if there's no overlap between valves opened by me and valves opened by the elephant,
# we have a candidate. Find the max such candidate.
best = max(
    valveset_score[valves1] + valveset_score[valves2]
    for valves1, valves2 in combinations(valveset_score, 2)
    if valves1.isdisjoint(valves2)
)
print(best)