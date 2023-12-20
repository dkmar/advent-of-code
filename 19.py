#!/usr/bin/env python3
from lib import *

# 21:00
infile = sys.argv[1] if len(sys.argv)>1 else '19.in'
f = open(infile, 'r') if infile != '-' else sys.stdin

# lines = list(map(Input, f))
data = Input(f.read().rstrip())
lines, ratings = data.split('\n\n')
#grid = Grid.from_text(data)
#grid = ZGrid.from_text(f.read().rstrip())
'''
ft{m<1347:R,m<1967:A,A}
gbv{x<51:R,R}
lks{m<2978:kgl,a<680:ntb,x<577:hzp,mg}
db{a>2314:R,A}
rml{a<479:R,m>2803:A,R}
'''

def range_of(op: str, val: int):
    # <1347 -> [1, 1347)
    if op == '<':
        return P.closedopen(1, val)
    else:
        return P.closedopen(val+1, 4000+1)

workflows = defaultdict(list)
for line in map(Input, lines.splitlines()):
    workflow_name, *rest = line.tokenize('{,}')
    workflow = workflows[workflow_name]
    for x in rest[:-1]:
        x, dst = x.split(':')
        part, op, v = x[0], x[1], x[2:]
        workflow.append((dst, part, range_of(op, int(v))))
    workflow.append(rest[-1])

def part1(p1 = 0):
    def get_part_ratings():
        for prs in ratings.splitlines():
            prs = prs.strip('{}').split(',')
            prs = (pr.split('=') for pr in prs)
            part_ratings = {
                part: int(rate)
                for part, rate in prs
            }
            yield part_ratings

    def xmas(W: str, rates: dict[str, int]) -> int:
        match W:
            case 'A':
                return sum(rates.values())
            case 'R':
                return 0
            case _:
                workflow = workflows[W]
                for dst, part, admit_range in workflow[:-1]:
                    if rates[part] in admit_range:
                        return xmas(dst, rates)
                # otherwise default transition
                return xmas(workflow[-1], rates)

    return sum(xmas('in', rates) for rates in get_part_ratings())


def part2(p2 = 0):
    def interval_size(interval: P.Interval):
        if interval.empty:
            return 0
        assert isinstance(interval.upper, int) and isinstance(interval.lower, int)
        return interval.upper - interval.lower

    # n from px (a_range) -> qkq:
    #    a_range & 1..<2006
    # this function should prob be called num_accepted
    def xmas(W: str, rates: dict[str, P.Interval]) -> int:
        match W:
            case 'A':
                return math.prod(map(interval_size, rates.values()))
            case 'R':
                return 0
            case _:
                ways = 0
                workflow = workflows[W]
                for dst, part, admit_range in workflow[:-1]:
                    if intersection := rates[part] & admit_range:
                        ways += xmas(dst, rates.copy() | {part: intersection})
                        rates[part] -= intersection

                ways += xmas(workflow[-1], rates)
                return ways

    rates = {
        part: P.closedopen(1, 4000+1)
        for part in 'xmas'
    }
    return xmas('in', rates)


print(f'Part 1: {part1()}')
print(f'Part 2: {part2()}')
