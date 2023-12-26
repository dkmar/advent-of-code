#!/usr/bin/env python3
from lib import *

# 16:45
infile = sys.argv[1] if len(sys.argv)>1 else '20.in'
f = open(infile, 'r') if infile != '-' else sys.stdin

lines = list(map(Input, f))
part1 = part2 = 0
'''
%fg -> nt, gt
&zp -> rx
%fh -> nt, xz
%pj -> zj, zq
%jc -> nt, nk

broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a

machine [mod]-cable-[mod] machine
pulse = high | low
flip-flop := on/off; high>None, low>on/off ^ 1 and flip on/off
conjunction := [prev]; low>high and sets prev, high>all(high)? low : high
want: total # of lows and highs sent
'''
@dataclasses.dataclass
class Module:
    type: str
    state: int
    dsts: list[str]

module_lookup = {'button': Module('', 0, dsts = ['broadcaster'])}
parents = defaultdict(dict)
for line in lines:
    src, _, *dsts = line.drop('%&,').split()
    module_lookup[src] = module = Module(line[0], 0, dsts)
    for dst in dsts:
        parents[dst] |= {src: len(parents[dst])}

# rx <- zp
rx_parent = next(iter(parents['rx']))
# zp <- (sb, nd, ds, hf)
rx_conditions_needed = len(parents[rx_parent])
# cycle number when an rx condition was met.
rx_condition_met = {}

def solve(cycles = 1000, part1=0, part2=0):
    cnts = [0, 0]
    for c in range(1, cycles+1):
        # (dst, pulse, src?)
        q = deque([('button', 0, None)])
        while q:
            mod, pulse, src = q.popleft()
            # print(f'{src} -{pulse}-> {mod}')
            module = module_lookup.get(mod)
            if not module:
                continue

            match module.type:
                case '%':
                    if pulse: continue
                    pulse = module.state ^ 1
                    module.state ^= 1
                case '&':
                    # check if any rx conditions have been cleared for part2
                    if mod == rx_parent and pulse:
                        # print(c, mod, f'{module.state:04b}', f'<- {pulse} from {src}')
                        rx_condition_met.setdefault(src, c)
                        if len(rx_condition_met) == rx_conditions_needed:
                            # all cleared. find when they coinside.
                            part2 = math.lcm(*rx_condition_met.values())
                            return part1, part2
                    # set as 0: module.state &= ~(1 << parents[mod][src])
                    # set as pulse: module.state |= (pulse << parents[mod][src])
                    module.state &= ~(1 << parents[mod][src])
                    module.state |= (pulse << parents[mod][src])
                    pulse = int(module.state != (1 << len(parents[mod]))-1)

            for dst in module.dsts:
                cnts[pulse] += 1
                q.append((dst, pulse, mod))

            if c == 1000:
                part1 = cnts[0] * cnts[1]

part1, part2 = solve(cycles=10_000)
print(f'Part 1: {part1}')
print(f'Part 2: {part2}')
