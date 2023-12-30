#!/usr/bin/env python3
from lib import *
sys.setrecursionlimit(10**4)

# 21:00
infile = sys.argv[1] if len(sys.argv)>1 else '23.in'
f = open(infile, 'r') if infile != '-' else sys.stdin

data = Input(f.read().rstrip())
grid = ZGrid.from_text_with_drop(data, '#')
'''
#.##########################################################
#.............#...#...###...#...#.......#...###...#...#...#.
#############.#.#.#.#.###.#.#.#.#.#####.#.#.###.#.#.#.#.#.#.
#.............#.#...#.#...#.#.#...#.....#.#...#.#.#.#.#.#.#.
#.#############.#####.#.###.#.#####.#####.###.#.#.#.#.#.#.#.
'''
up, down, left, right = ComplexCardinal.FOUR_DIRECTIONS
src = complex(1,0)
dst = complex(grid.n-2, grid.m-1)


def compress_graph(src: complex, dst: complex, neighbors_fn) -> dict:
    '''
    Let's do some path compression.

    Option 1:
        We could just include junctions (corners, 3+ intersections).
    Option 2:
        We do the same but omit corners as we can assume corners will be taken by the path.
        Just include the 3+ edge intersections.

    Option 1 yields 2k+ vertices whereas Option 2 leaves us only 36. Let's do option 2.
    '''
    # all junctions of 3+ degree (and also dst)
    relevant_locs = {
        loc for loc in grid.locs()
        if len(list(neighbors_fn(loc))) > 2
    } | {dst}

    graph = defaultdict(list)
    seen = {src}
    q = deque([src])
    while q:
        loc = q.popleft()
        # consider the next relevant location in each branch
        for curr in neighbors_fn(loc):
            prev = loc
            dist = 1
            # find next relevant location if there is one
            while curr and curr not in relevant_locs:
                prev, curr = curr, next(
                    (nbr for nbr in neighbors_fn(curr) if nbr != prev),
                    None
                )
                dist += 1

            if curr is not None:
                # add edge and enqueue for exploration.
                graph[loc].append((curr, dist))
                if curr not in seen:
                    seen.add(curr)
                    q.append(curr)

    return graph


def longest_hike(graph: dict, src: complex, dst: complex) -> int:
    visited = set()
    def find_hikes(loc: complex, length: int):
        if loc == dst:
            yield length
            return

        visited.add(loc)
        for nbr, dist in graph[loc]:
            if nbr not in visited:
                yield from find_hikes(nbr, length + dist)
        visited.remove(loc)

    return max(find_hikes(src, 0))


def part1():
    def neighbors(loc: complex):
        # constrain neighbors if this is a slope.
        if (ch := grid[loc]) in '^v<>':
            dir = ComplexCardinal.FOUR_DIRECTIONS['^v<>'.index(ch)]
            if (nbr := loc + dir) in grid:
                yield nbr
            return

        for dir in up, down, left, right:
            if (nbr := loc + dir) in grid:
                yield nbr

    graph = compress_graph(src, dst, neighbors_fn = neighbors)
    return longest_hike(graph, src, dst)


def part2():
    def neighbors(loc: complex):
        for dir in up, down, left, right:
            if (nbr := loc + dir) in grid:
                yield nbr

    graph = compress_graph(src, dst, neighbors_fn = neighbors)
    return longest_hike(graph, src, dst)


print(f'Part 1: {part1()}')
print(f'Part 2: {part2()}')
