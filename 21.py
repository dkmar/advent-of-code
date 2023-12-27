#!/usr/bin/env python3
from lib import *

# 14:26
infile = sys.argv[1] if len(sys.argv)>1 else '21.in'
f = open(infile, 'r') if infile != '-' else sys.stdin
data = Input(f.read().rstrip())
grid = ZGrid.from_text(data)
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

def explore(locs: set, steps: int):
    for s in range(steps):
        next_locs = set()
        for loc in locs:
            for dir in up, down, left, right:
                if grid.get(next_loc := loc + dir, ROCK) == GARDEN:
                    next_locs.add(loc + dir)
        locs = next_locs
    return locs

def part1():
    grid[src] = '.'
    reachable = explore({src}, 64)
    # having start labeled 'S' makes for easier part2 exploration.
    grid[src] = 'S'
    return len(reachable)

class InfiniteGrid:
    def __class_getitem__(cls, loc: complex, m=grid.m, n=grid.n):
        # make src (0,0) and return modded
        return grid[loc % (n, m)]

def explore_infinite(locs: set, steps: int):
    for s in range(steps):
        next_locs = set()
        for loc in locs:
            # for dir in up, down, left, right:
            for dir in up, down, left, right:
                ch = InfiniteGrid[next_loc := loc + dir]
                if ch == GARDEN or ch == 'S':
                    next_locs.add(next_loc)
        locs = next_locs
    return locs

def diamond_analysis(k: int):
    ''' (see part2 function for notes)
    Valid diamond is defined by (65 + 131k) steps from the src.

    Return:
        Breakdown of type A diamonds, type B diamonds, and garden plot total.

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
    def count_A(reach: set, start: complex):
        cnt = 0
        for loc in reach:
            relative_loc = loc - start
            if abs(relative_loc.x) + abs(relative_loc.y) <= 65:
                cnt += 1

        return cnt

    def count_B(reach: set, b_box: tuple):
        # a1 a2
        #   b
        # a3 a4
        a1, a2, a3, a4 = b_box
        # make the center of this B the average of its corners.
        b = complex((a1.x+a2.x+a3.x+a4.x)/4, (a1.y+a2.y+a3.y+a4.y)/4)

        cnt = 0
        for loc in reach:
            relative_loc = loc - b
            if abs(relative_loc.x) + abs(relative_loc.y) <= 65:
                cnt += 1

        return cnt

    def get_A_starts(start: complex, n: int):
        row_offset = n//2
        for row in range(-row_offset, row_offset+1):
            col_offset = n//2 - abs(row)
            for col in range(-col_offset, col_offset+1):
                yield start + complex(col * 131, row * 131)


    def get_B_box(A_starts: Iterable):
        # A A
        #  B
        # A A
        #  B
        # A A

        # Each pair per row can form two of corners "bounding"" a B diamond above and below
        ordered_A_starts = sorted(A_starts, key=lambda c: (c.y, c.x))
        for a1, a2 in pairwise(ordered_A_starts[1:-1]):
            if a1.y != a2.y:
                continue

            # box for B above
            yield (
                a1 + (0-131j), a2 + (0-131j),
                a1, a2
            )
            # box for B below
            yield (
                a1, a2,
                a1 + (0+131j), a2 + (0+131j)
            )


    cntsA, cntsB = defaultdict(int), defaultdict(int)
    # n = 2 * k + 1. get all start positions of type A diamonds with center width n
    A_starts = list(get_A_starts(src, 2 * k + 1))

    reach = explore_infinite({src}, 65 + 131 * k)
    cntsA = Counter(count_A(reach, start) for start in A_starts)
    cntsB = Counter(count_B(reach, b_box) for b_box in set(get_B_box(A_starts)))

    total = sum(a * cnt for a, cnt in cntsA.items()) + sum(b * cnt for b, cnt in cntsB.items())
    assert total == len(reach)

    # Breakdown of type A diamonds, type B diamonds, and garden plot total.
    # (Counter({3784: 4, 3678: 1}), Counter({3706: 2, 3727: 2}), 33680)
    return cntsA, cntsB, total


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

    A: (primary diamond) 7463 possible
    B: (diamond composed of the four corners() 7433 possible
    A ={
        A1: 3678
        A2: 3784
    }
    B ={
        B1: 3727
        B2: 3706
    }

    65 S 65+65 S 65+65 S 65
    aka 131s for A-type diamonds.

    65 + 131k
    65 + 131 * 0:
        Counter({3784: 1})
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
    B: k^2+k, k^2+k

    26501365 = 65 + 131 * 2023_00
    '''
    # uncomment to see analysis results
    # for k in 0,1,2:
    #     res = diamond_analysis(k)
    #     print(res)

    diamond_info = diamond_analysis(1)
    A1_total, A2_total = diamond_info[0].keys()
    B12_total = sum(diamond_info[1].keys())

    # 3784*a1 + 3678*a2 + (3727 + 3706)*b
    target_k = (NEED_STEPS - 65) // 131  # 2023_00
    a1 = (target_k+1)**2
    a2 = target_k*target_k
    A_total = A1_total * a1 + A2_total * a2
    b = target_k*target_k + target_k
    B_total = B12_total * b
    return A_total + B_total

print(f'Part 1: {part1()}')
print(f'Part 2: {part2()}')
