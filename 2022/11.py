#!/usr/bin/env python3
from math import prod
from util import get_ints
import sys
from collections import defaultdict
infile = sys.argv[1] if len(sys.argv)>1 else '11.in'
with open(infile, 'r') as f:
    data = f.read().strip()
    monkeys = data.split('\n\n')
    # lines = list(map(str.strip, f.readlines()))

'''
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3
'''
bags, ops, tests = [], [], []
for monkey in monkeys:
  info = monkey.splitlines()
  bags.append(get_ints(info[1]))
  ops.append(eval('lambda old: '+ info[2].split(' = ')[-1]))
  tests.append(get_ints(''.join(info[3:])))

n = len(bags)
factor = prod(t[0] for t in tests)
inspected = [0]*n

for _ in range(10_000):
  for i in range(n):
    for _ in range(len(bags[i])):
      w = bags[i].pop()
      d,dst_true,dst_false = tests[i]

      w = ops[i](w) % factor
      # w //= 3

      if w%d == 0:
        bags[dst_true].append(w)
      else:
        bags[dst_false].append(w)

      inspected[i] += 1

top = sorted(inspected)
print(top[-1]*top[-2])