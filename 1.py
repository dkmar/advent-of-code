# !/usr/bin/env python3
import lib
import sys, math, re
import numpy as np
from collections import defaultdict, deque, Counter

# 13:35 - 14:46

infile = sys.argv[1] if len(sys.argv) > 1 else '1.in'
with open(infile, 'r') as f:
    # data = f.read().strip()
    lines = list(map(str.strip, f))
    # grid = list(list(ln) for ln in map(str.strip, f.readlines()))

'''
ninefourone1
53sevenvvqm
kscpjfdxp895foureightckjjl1
72fivebt9ndgq
28gtbkszmrtmnineoneightmx
'''


def part2():
    digit_spellings = 'one two three four five six seven eight nine'.split()
    digit_strs = [str(d) for d in range(1, 10)]

    digit_from_str = dict(zip(digit_spellings, digit_strs)) \
                     | dict(zip(digit_strs, digit_strs))

    pattern = re.compile(r'(?=([1-9]|one|two|three|four|five|six|seven|eight|nine))', re.IGNORECASE)
    calibration_values = []
    for line in lines:
        digits = pattern.findall(line)
        a, b = digits[0], digits[-1]

        vals = digit_from_str[a] + digit_from_str[b]
        calibration_values.append(int(vals))

    answer2 = sum(calibration_values)
    print(f'part 2: {answer2}')


def part1():
    pattern = re.compile(r'[1-9]')
    calibration_values = []
    for line in lines:
        digits = pattern.findall(line)
        a, b = digits[0], digits[-1]

        vals = a + b
        calibration_values.append(int(vals))

    answer1 = sum(calibration_values)
    print(f'part 1: {answer1}')


part1()
part2()
