#!/usr/bin/env python3
from lib import *

# 01:13
infile = sys.argv[1] if len(sys.argv) > 1 else "18.in"
f = open(infile, "r") if infile != "-" else sys.stdin
lines = list(map(Input, f))
"""
L 4 (#906400)
D 13 (#01d963)
L 3 (#79a0e0)
U 10 (#98a913)
L 2 (#19c840)

+ is safe to count
? is where the segment is contested and we need to ensure it's counted once.
these (and the ends too) will be our y-values that partition our polygon.
We refer to this partitioning line as the horizon below.

####### +<
#.....# +
###...# ?
..#...# +
..#...# +
###.### ?
#...#.. +
##..### ?
.#....# +
.###### +<
"""
DIR = dict(zip("UDLR", ComplexCardinal.FOUR_DIRECTIONS))
Event = namedtuple('Event', ['loc', 'is_end'])

def sweep_trenches(events: Sequence[Event]) -> int:
    # line sweep. "horizon" is a horizontal line cutting our verticals.
    contested_portion = {ev.loc.y: P.empty() for ev in events}
    events = deque(sorted(
        events,
        key=lambda ev: ev.loc.y
    ))

    area = 0
    active = SortedKeyList(key=lambda ev: ev.loc.x)
    while events:
        # advance horizon
        horizon = events[0].loc.y
        while events and events[0].loc.y == horizon:
            ev = events.popleft()
            if ev.is_end:
                active.pop(active.bisect_key_left(ev.loc.x))
            else:
                active.add(ev)

        if not active:
            # we're done
            assert bool(active) == bool(events)
            break

        y1, y2 = horizon, events[0].loc.y
        for a, b in batched(active, 2):
            x1, x2 = a.loc.x, b.loc.x
            # (y1, y2) * [x1, x2]. exclude start and end lines; count them later.
            area += (y2 - (y1+1)) * (x2+1 - x1)
            # contested range of y1 and y2. we need to ensure count once.
            contested_range = P.closed(x1, x2)
            contested_portion[y1] |= contested_range
            contested_portion[y2] |= contested_range

    def count_segment_once(segment: P.Interval):
        # make LSP happy
        assert isinstance(segment.upper, float) and isinstance(segment.lower, float)
        assert segment.right == P.CLOSED
        return segment.upper+1 - segment.lower

    area += sum(
        sum(map(count_segment_once, segments))
        for segments in contested_portion.values()
    )
    return int(area)


def generate_events(parsed_instructions: Iterable) -> list[Event]:
    # Event = namedtuple('Event', ['loc', 'is_end'])
    events = []
    curr = 0+0j
    for direction, count in parsed_instructions:
        prev = curr
        curr += DIR[direction] * count
        match direction:
            case 'U':
                start, end = curr, prev
                events += Event(start, False), Event(end, True)
            case 'D':
                start, end = prev, curr
                events += Event(start, False), Event(end, True)

    return events

def part1():
    parts = (line.drop("(#)").split() for line in lines)
    inst = [(direction, int(count))
            for direction, count, _ in parts]

    events = generate_events(inst)
    return sweep_trenches(events)


def part2():
    colors = (line.split()[-1].strip("(#)") for line in lines)
    inst = [("RDLU"[int(color[-1])], int(color[:5], 16))
            for color in colors]

    events = generate_events(inst)
    return sweep_trenches(events)

print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
