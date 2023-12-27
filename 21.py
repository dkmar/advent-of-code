#!/usr/bin/env python3
from lib import *

# 14:26
infile = sys.argv[1] if len(sys.argv)>1 else '21.in'
f = open(infile, 'r') if infile != '-' else sys.stdin

# lines = list(map(Input, f))
data = Input(f.read().rstrip())
#a, b = data.split('\n\n')
grid = ZGrid.from_text(data)
#grid = ZGrid.from_text_with_transform(data, int)
'''
............................................................
.#....................#..#......##.#..#.#..#.#..#.#.........
.........#......#.#.........#...#.#...##..#.......#..#......
..#...#...#..#..#.#..#......#.....#...#....##...............
............#................#...#.............#............
'''
GARDEN = '.'
ROCK = '#'
NEED_STEPS = 26501365



up, down, left, right = ComplexCardinal.FOUR_DIRECTIONS
src = grid.find('S') or complex()
# grid[src] = '.'
class InfiniteGrid:
    def __class_getitem__(cls, loc: complex, m=grid.m, n=grid.n):
        # make src (0,0) and return modded
        return grid[loc % (n, m)]

def explore(locs: set, steps: int):
    for s in range(steps):
        next_locs = set()
        for loc in locs:
            for dir in up, down, left, right:
                if grid.get(next_loc := loc + dir, ROCK) == GARDEN:
                    next_locs.add(loc + dir)
        locs = next_locs
    return locs

def explore_infinite(locs: set, steps: int):
    for s in range(steps):
        next_locs = set()
        for loc in locs:
            # for dir in up, down, left, right:
            for dir in up, down, left, right:
                # if (loc + dir) == (196+65j) and (196+65j) not in next_locs and (196+65j) not in locs:
                #     print(f'Adding it. {s+1}')
                    # breakpoint()
                ch = InfiniteGrid[next_loc := loc + dir]
                if ch == GARDEN or ch == 'S':
                    next_locs.add(next_loc)
                    # print('S', next_loc, next_loc % (grid.n, grid.m))
        locs = next_locs

    return locs


def part1():
    reachable = explore({src}, 64)
    return len(reachable)

def part2():
    '''
    Notably, we have this relationship:
        (target_steps - 65) % 131 == 0

    Essentially we end up with

            1
        2       3
    4       5       6
        7       8
            9

    where each of these is a full diamond and 5 is the center diamond (covered with 65 steps).

    and the base diamond shape:
        UL      UR
            D
        BL      BR

    UL {:65-i, :65}
    UR {65+i:, :65}
    BL {:i-65, 65:}
    BR {65+130-i:, 65:}

    New diamonds are either a construction of D or (BR + BL
                65 + 131                            TR + TL)

                A
            B       B
        A       A       A
            B       B
                A

                65 + 131 + 131
                A
            B       B
        A       A       A
    B       B       B       B
A       A       A       A       A
    B       B       B       B
        A       A       A
            B       B
                A

                A
            B       B
        A       A       A
    B       B       B       B
A       A       A       A       A
    B       B       B       B
        A       A       A
            B       B
                A

    (34150 - 5 * 3678) / 4 = 3940
    (93366 - 13* 3678) / 12 = 3796

    7463 7433
    7463 ={
        even: 3678
        odd: 3784
    }
    7433 ={
        B1: 3727
        B2: 3641
        B3: 3706
        B4: 3662
    }

    65 S 65+65 S 65+65 S 65
    aka 131s for A-type diamonds.

    65 + 131k
    65 + 131 * 1:
        Counter({3784: 4, 3678: 1})
        Counter({3727: 2, 3706: 2})
    65 + 131 * 2:
        Counter({3784: 9, 3678: 4})
        Counter({3727: 6, 3706: 6})
    65 + 131 * 3:
        Counter({3784: 16, 3678: 9})
        Counter({3727: 12, 3706: 12})


    A: (k+1)^2, k^2
    B: k*2 - 1, k*2 - 1, k*2 - 1, k*2 - 1

    26501365 = 65 + 131 * 2023_00
    '''
    # def get_primary_diamond_count():
    # def classify(x: int, y: int) -> int:
    #     if abs(x) + abs(y) <= 65:
    #         return 2
    #     else:
    #         return 0


    #     if y <= 65:
    #         if x < y:
    #             return 0
    #         elif x >= 65 + y:
    #             return 1
    #     elif x < y - 65:
    #         return 3
    #     elif x >= 65+130 - y:
    #         return 4

    #     return 2
    def count_B(reach: set, b_box: tuple):
        '''
                A
            B       B
        A       A       A
    B       B       B       B
A       A       A       A       A
    B       B       B       B
        A       A       A
            B       B
                A
        '''
        a1, a2, a3, a4 = b_box
        b = complex((a1.x+a2.x+a3.x+a4.x)/4, (a1.y+a2.y+a3.y+a4.y)/4)
        for a in a1, a2, a3, a4:
            dz = a - b
            d = abs(dz.real) + abs(dz.imag)
            print(f'{b}<-->{a} {d}')

        cnt = 0
        for loc in reach:
            relative_loc = loc - b
            if abs(relative_loc.x) + abs(relative_loc.y) < 66:
                for S_loc in a1, a2, a3, a4:
                    relative_loc = loc - S_loc
                    if abs(relative_loc.x) + abs(relative_loc.y) <= 65:
                        break
                else:
                    cnt += 1

        return cnt

    def count_A(reach: set, start: complex):
        cnt = 0
        for loc in reach:
            relative_loc = loc - start
            if abs(relative_loc.x) + abs(relative_loc.y) <= 65:
                cnt += 1

        return cnt

    def get_starts(start: complex, n: int):
        row_offset = n//2
        for row in range(-row_offset, row_offset+1):
            col_offset = n//2 - abs(row)
            for col in range(-col_offset, col_offset+1):
                yield start + complex(col * 131, row * 131)
        # starts = {
        #     start - complex(0, -)
        # ]
    # centerOdd = explore_infinite({src}, 65)
    # count(centerOdd, src)
    # offCenterOdd = explore_infinite({src + (65+131j)}, 65)
    # count(offCenterOdd, src + (65+131j))
    # for start_offset in complex(-131,0), complex(0,0), complex(131,0):
    # for start_offset in complex(0, -131), complex(0,0), complex(0,131):
    # reach = explore_infinite({src}, 65 + 131 + 131)
    # import pickle
    # pickle.l

    def get_B_box(A_starts: Iterable):
        # A A
        #  B
        # A A
        #  B
        # A A
        core = sorted(A_starts, key=lambda c: (c.y, c.x))
        print(core)
        prev = None
        for a1, a2 in pairwise(core[1:]):
            if prev is None:
                yield (
                    a1 + (0-131j), a2 + (0-131j),
                    a1, a2
                )
                yield (
                    a1, a2,
                    a1 + (0+131j), a2 + (0+131j)
                )
            elif a1.y != a2.y:
                a1, a2 = prev
                yield (
                    a1 + (0-131j), a2 + (0-131j),
                    a1, a2
                )
                yield (
                    a1, a2,
                    a1 + (0+131j), a2 + (0+131j)
                )

                prev = None
                continue
            else:
                yield (
                    a1 + (0-131j), a2 + (0-131j),
                    a1, a2
                )
                yield (
                    a1, a2,
                    a1 + (0+131j), a2 + (0+131j)
                )

            prev = a1, a2


    cntsA, cntsB = defaultdict(int), defaultdict(int)
    A_starts = list(get_starts(src, 3))
    print(len(A_starts))

    reach = explore_infinite({src}, 65 + 131 * 1)
    for start in A_starts:
        # start = src + start_offset
        print('Start', start, len(reach))
        print(f'A: {(cnt := count_A(reach, start))}')
        cntsA[cnt] += 1
    print(cntsA)

    for b_box in set(get_B_box(A_starts)):
        print('B Box', b_box, int((b_box[0].y + 0.5) / 131))
        print(f'B: {(cnt := count_B(reach, b_box))}')
        cntsB[cnt] += 1
    print(cntsB)

    tot = sum(a * cnt for a, cnt in cntsA.items()) + sum(b * cnt for b, cnt in cntsB.items())
    print('Total: ', tot)

    # center_plus_layer1Even = explore_infinite({src}, 64 + 131)
    # count(center_plus_layer1Even, src)
    # offCenter_plus_layer1Even = explore_infinite({src + (65+131j)}, 64 + 131)
    # count(offCenter_plus_layer1Even, src + (65+131j))
    # offCenter_plus_layer1Even = explore_infinite({src + (-65+131j)}, 64 + 131)
    # count(offCenter_plus_layer1Even, src + (-65+131j))

    # center_plus_layer1Even = explore_infinite({src}, 65 + 131)
    # count(center_plus_layer1Even, src)
    # offCenter_plus_layer1Even = explore_infinite({src + (65+131j)}, 65 + 131)
    # count(offCenter_plus_layer1Even, src + (65+131j))

    # center_plus_layer1Even = explore_infinite({src}, 66 + 131)
    # count(center_plus_layer1Even, src)
    # offCenter_plus_layer1Even = explore_infinite({src + (65+131j)}, 66 + 131)
    # count(offCenter_plus_layer1Even, src + (65+131j))

    # center_plus_layer2Odd = explore_infinite({src}, 65 + 131 + 131)
    # count(center_plus_layer2Odd, src)
    # offCenter_plus_layer2Odd = explore_infinite({src + (65+131j)}, 65 + 131 + 131)
    # count(offCenter_plus_layer2Odd, src + (65+131j))

    return 0

def segment(covered: set[complex]):
    # cover entirety of: half + full diamond + half
    full_range = 0
    # covered = sorted(covered)
    # psums = accumulate()

def project_plot():
    # (n - 65) % 131 == 0
    assert grid.m == grid.n
    size = grid.m
    radius = size // 2
    # cover entirety of: half + full diamond + half
    selection = radius * 3
    # covered = explore({src}, selection)
    for a in 0, 1, 2:
        covered = explore({src}, 65 + a * 131)
        print(len(covered))

    # lets segment this

# for loc in grid.locs():
#     relative_loc = loc - src
#     if not (abs(relative_loc.x) + abs(relative_loc.y) <= 65):
#         grid[loc] = '~'

# grid.print()

# project_plot()
# print(f'm {grid.m}, n {grid.n}')
# for want in 64, 65,66,130,131:
#     got = explore_infinite({src}, want)
#     print(want, len(got))

# what if we do bfs from every spot on the border and get the state after
# def take_steps2(locs: set, steps: int):
#     # key = loc % (grid.n, grid.m)
#     # if entry := memo:
#     #     return entry
#     for step in range(steps):
#         next_locs = set()
#         for loc in locs:
#             for dir in up, down, left, right:
#                 if InfiniteGrid[next_loc := loc + dir] == GARDEN:
#                     next_locs.add(loc + dir)
#         locs = next_locs
#     return locs

# print(len(even))
# for loc, times in reached_with.items():
#     # print(grid[loc], times)
#     part1 += any(tm % 2 == 0 for tm in times)
# print(src)
# print(sum(len(x) for x in reached_with.values()))
# part1 = len(take_steps({src}, 64))
# part2 = len(take_steps({src}, 100))

# A = list(itertools.combinations_with_replacement([3678, 3679, 3784, 3785], r=25))
# B = list(itertools.combinations_with_replacement([3661, 3662, 3640, 3641, 3792, 3793, 3771, 3772], r=24))

# #
# targets =  33680, 93366, 182842
# for As in A:
#     for Bs in B:
#         if (s := sum(chain(As, Bs))) in targets:
#             print(s)
#             print(Counter(As), Counter(Bs))
#             break
#     else:
#         continue

#     break
        # print(sum(chain(As, Bs)))
# print(f'Part 1: {part1()}')
for k in 1, 2, 3, 2023_00:
    A1 = (k+1)**2
    A2 = k*k
    A_total = A1 * 3784 + A2 * 3678
    Bn = k*k+k
    B_total = Bn * (3727 + 3706)
    print('\t', A1, A2)
    print('\t', Bn)
    print(f'65+131*{k}', A_total + B_total)
# print(f'Part 2: {part2()}')
# def get_starts(start: complex, n: int):
#     row_offset = n//2
#     for row in range(-row_offset, row_offset+1):
#         col_offset = n//2 - abs(row)
#         for col in range(-col_offset, col_offset+1):
#             yield start + complex(col * 131, row * 131)

# for start in get_starts(src, 5):
#     assert InfiniteGrid[start] == 'S'
#     print(start)
print('Done')
