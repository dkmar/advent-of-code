#!/usr/bin/env python3
import lib
import sys, math, re, functools, operator
import numpy as np
from collections import defaultdict, deque, Counter

# 15:11 1527 1532

infile = sys.argv[1] if len(sys.argv)>1 else '2.in'
with open(infile, 'r') as f:
    #data = f.read().strip()
    lines = list(map(str.strip, f.readlines()))
    #grid = list(list(ln) for ln in map(str.strip, f.readlines()))

'''
Game 1: 7 blue, 5 red; 10 red, 7 blue; 5 blue, 4 g
Game 2: 8 green, 3 red; 7 blue, 6 red, 8 green; 7 
Game 3: 6 blue, 3 red, 7 green; 3 red, 3 green, 8 
Game 4: 3 red, 4 green; 5 red, 1 blue; 2 green; 3 
Game 5: 17 red, 5 blue, 3 green; 8 green, 9 red, 1
'''


def get_game(line: str):
    part1, part2 = line.split(':')
    game_id = int(part1[5:])

    cube_counts = defaultdict(int)
    pattern = re.compile(r'(\d+) ([^,;]+)')
    for cnt, color in pattern.findall(part2):
        cnt = int(cnt)
        cube_counts[color] = max(cube_counts[color], cnt)

    return game_id, cube_counts

def part1():
    limit = {'red': 12, 'green': 13, 'blue': 14}
    res = 0
    for line in lines:
        game_id, cube_counts = get_game(line)

        for color, max_cnt in limit.items():
            if cube_counts[color] > max_cnt:
                break
        else:
            res += game_id

    print('part1: ', res)

def part2():
    res = 0
    for line in lines:
        game_id, cube_counts = get_game(line)
        power = cube_counts['red'] * cube_counts['green'] * cube_counts['blue']
        res += power
        
    
    print('part2: ', res)
    
part1()
part2()