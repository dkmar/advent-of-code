#!/usr/bin/env python3
import util
import sys, math, re, functools, operator, itertools, bisect
import numpy as np
from collections import defaultdict, deque, Counter

# 21:00

infile = sys.argv[1] if len(sys.argv) > 1 else '7.in'
f = open(infile, 'r') if infile != '-' else sys.stdin

# data = f.read().strip()
lines = list(map(str.strip, f))
# grid = list(list(ln) for ln in map(str.strip, f))

'''
6A868 562
KAKKA 232
39399 272
2J722 48
5AQ36 444
'''
entries = [(hand, int(bid))
           for hand, bid in map(str.split, lines)]


def kind_rank(counts: Counter):
    match len(counts):
        case 1:
            return 1
        case 2:
            if max(counts.values()) == 4:
                return 2
            else:
                return 3
        case 3:
            if max(counts.values()) == 3:
                return 4
            else:
                return 5
        case 4:
            return 6
        case 5:
            return 7


def card_rank(hand: str, order: str):
    return tuple(order.index(h) for h in hand)


@functools.cache
def key_pt1(hand: str):
    counts = Counter(hand)
    order = ' AKQJT98765432'
    return (kind_rank(counts), *card_rank(hand, order=order))


@functools.cache
def key_pt2(hand: str):
    counts = Counter(hand)

    if len(counts) > 1 and 'J' in hand:
        most_frequent = next(ch for ch, _ in counts.most_common() if ch != 'J')
        counts = Counter(hand.replace('J', most_frequent))

    order = ' AKQT98765432J'
    return (kind_rank(counts), *card_rank(hand, order=order))


def total_winnings(entries: list, keyfn: callable):
    entries.sort(key=lambda e: keyfn(e[0]), reverse=True)
    return sum(rank * bid
               for rank, (hand, bid) in enumerate(entries, 1))


part1 = total_winnings(entries, key_pt1)
part2 = total_winnings(entries, key_pt2)
print(f'part 1: {part1}')
print(f'part 2: {part2}')
