#!/usr/bin/env python3
import util
import sys, math
from collections import defaultdict, deque
from functools import cache

# 15:32
ORE, CLAY, OBSIDIAN, GEODE = 0, 1, 2, 3
infile = sys.argv[1] if len(sys.argv)>1 else '19.in'
with open(infile, 'r') as f:
    #data = f.read().strip()
    lines = list(map(str.strip, f.readlines()))
    blueprint = {}
    for fields in map(util.get_ints, lines):
        blueprint_id = fields[0]
        costs = [[0]*4 for _ in range(4)]
        costs[ORE][ORE] = fields[1]
        costs[CLAY][ORE] = fields[2]
        costs[OBSIDIAN][ORE] = fields[3]
        costs[OBSIDIAN][CLAY] = fields[4]
        costs[GEODE][ORE] = fields[5]
        costs[GEODE][OBSIDIAN] = fields[6]
        blueprint[blueprint_id] = costs
    #grid = list(list(ln) for ln in map(str.strip, f.readlines()))

'''
Blueprint 1: Each ore robot costs 3 ore. Each clay
Blueprint 2: Each ore robot costs 4 ore. Each clay
Blueprint 3: Each ore robot costs 4 ore. Each clay
Blueprint 4: Each ore robot costs 3 ore. Each clay
Blueprint 5: Each ore robot costs 4 ore. Each clay
'''

MINS = 24
BOT_TYPES = range(4)

def can_build(mats, costs):
    return all(m >= c for (m,c) in zip(mats, costs))

def score_upperbound(geodes, geode_robots, time):
    '''
    the most geodes possible would be those mined plus 1 per robot per minute,
    plus assuming we can buy another geode robot every minute.
    '''
    return geodes + geode_robots * time + sum(range(time))

def solve(blueprint_id, time=24):
    bot_costs = blueprint[blueprint_id]
    max_needed = [
        max(bot_cost[0] for bot_cost in bot_costs),
        bot_costs[OBSIDIAN][CLAY],
        bot_costs[GEODE][OBSIDIAN],
        sys.maxsize
    ]

    seen = set()
    best = 0
    q = [((0,0,0,0),(1,0,0,0),time,0)] # materials, robots, time, passed
    
    while q:
        mats, robots, time, passed = state = q.pop()

        state = state[:-1] 
        if state in seen:
            continue
        seen.add(state)

        next_mats = tuple(m + rc for (m,rc) in zip(mats, robots))
        time -= 1
    
        if time == 0:
            best = max(best, next_mats[GEODE])
            continue

        # if there's no way this state could improve our best, skip it.
        if score_upperbound(mats[-1], robots[-1], time+1) < best:
            continue

        built = 0
        for bot in BOT_TYPES:
            if can_build(mats, bot_costs[bot]) and robots[bot] < max_needed[bot] and not (1 << bot) & passed:
                built |= (1 << bot) 
                new_mats = tuple(m - c for (m,c) in zip(next_mats,bot_costs[bot]))
                new_robots = robots[:bot] + (robots[bot]+1,) + robots[bot+1:]
                q.append((new_mats, new_robots, time, 0))

        if mats[ORE] < max_needed[ORE] \
        or (robots[CLAY] and mats[CLAY] < max_needed[CLAY]) \
        or (robots[OBSIDIAN] and mats[OBSIDIAN] < max_needed[OBSIDIAN]):
            q.append((next_mats, robots, time, built))

    return best

# part 1
quality_scores = [bid * solve(bid, MINS) for bid in blueprint]
print(sum(quality_scores))

# part 2
score = math.prod(solve(bid, 32) for bid in [1,2,3])
print(score)