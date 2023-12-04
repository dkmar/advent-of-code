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

@cache
def heuristic(bid, bot, mats):
    '''
    I have no idea. Let's say don't build if we will have enough of that
    mat after two turns with current bots.

    Also don't build anything but geode if we're in the last two minutes. 
    '''
    costs = blueprint[bid]
    if bot == GEODE:
        return True

    future_mats = mats
    # future_mats = tuple(m + rc for (m,rc) in zip(mats,robots))
    return any(future_mats[bot] <= 2*bot_cost[bot] for bot_cost in costs)



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
        # sort by geodes, geode bots, time, reverse(bots), reverse(mats)
        # q.sort(key=lambda e: (e[0][GEODE], e[1][GEODE], e[2], tuple(reversed(e[1])), tuple(reversed(e[0]))))
        # q = q[-1000:]
        # for _ in range(len(q)):
        mats, robots, time, passed = state = q.pop()

        state = state[:-1]
        if state in seen:
            continue

        seen.add(state)
        time -= 1
    
        next_mats = tuple(m + rc for (m,rc) in zip(mats, robots))
        if time == 0:
            best = max(best, next_mats[GEODE])
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








@cache
def bot_timelines(blueprint_id, mats, robots, time):
    if time == 0:
        # if mats[GEODE] > 0:
        #     print(mats, robots)
        return mats[GEODE]

    bot_costs = blueprint[blueprint_id]

    # generate materials
    next_mats = tuple(m + rc for (m,rc) in zip(mats, robots))

    best = 0
    for bot in BOT_TYPES:
        if can_build(mats, bot_costs[bot]) and heuristic(blueprint_id, bot, mats):
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
    # score = bot_timelines(bid, (0,0,0,0), (1,0,0,0), MINS)
    score = solve(bid, MINS)
    # print(earliest)
    print(f'score = {score}')
    print(f'quality = {bid * score}')
    quality_scores.append(bid * score)

# quality_scores = [bid * bot_timelines(bid, (0,0,0,0), (1,0,0,0), MINS) for bid in blueprint]
print(sum(quality_scores))