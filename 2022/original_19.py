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

def updated_mats(mats, costs):
    return tuple(m - c for (m,c) in zip(mats,costs))

def score_upperbound(geodes, geode_robots, time):
    return geodes + geode_robots * time + sum(range(time))

@cache
def bot_timelines(blueprint_id, mats, robots, time):
    global best
    if time == 0:
        return mats[GEODE]
    elif score_upperbound(mats[-1], robots[-1], time) < best:
        return 0

    bot_costs = blueprint[blueprint_id]

    # generate materials
    next_mats = tuple(m + rc for (m,rc) in zip(mats, robots))

    for bot in BOT_TYPES:
        if can_build(mats, bot_costs[bot]):
            if not robots[bot]:
                if time < earliest[bot]:
                    break
                elif time > earliest[bot]:
                    earliest[bot] = time
                # print(f'SETTING EARLIEST TO {time}\n {mats} {robots}')

            new_mats = tuple(m - c for (m,c) in zip(next_mats,bot_costs[bot]))
            new_robots = robots[:bot] + (robots[bot]+1,) + robots[bot+1:]

            res = bot_timelines(blueprint_id, new_mats, new_robots, time - 1)
            best = max(best, res)

    if any(robots[bot] == 0 and earliest[bot] > time for bot in BOT_TYPES):
        return best
    return max(best, bot_timelines(blueprint_id, next_mats, robots, time-1))

mats = [0]*4
robots = [1,0,0,0]

# score = bot_timelines(1, (0,0,0,0), (1,0,0,0), 24)
# print(f'score = {score}')
# print(f'quality = {score}')
quality_scores = []
for bid in blueprint:
    earliest = [100, -1, -1, -1]
    best = 0
    score = bot_timelines(bid, (0,0,0,0), (1,0,0,0), MINS)
    print(earliest)
    print(f'score = {score}')
    print(f'quality = {bid * score}')
    quality_scores.append(bid * score)

# quality_scores = [bid * bot_timelines(bid, (0,0,0,0), (1,0,0,0), MINS) for bid in blueprint]
print(sum(quality_scores))