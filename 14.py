#!/usr/bin/env python3
from lib import *

# 19:28 1938
infile = sys.argv[1] if len(sys.argv) > 1 else '14.in'
f = open(infile, 'r') if infile != '-' else sys.stdin

# lines = list(map(Input, f))
data = Input(f.read())
grid = Grid.from_text(data)

'''
......O........#....O..O.O#O.O.##.O#.O##.O#......O........O.
O#..O...O....O.#...##.O....O..O.#...#...O..O#.#.#......#.O##
O....##.O#O##.O...#...#.#.......OO.##..###.OO..O.#.#.OO#O..#
....O#.O..OO.#..OOOO#.......O.....O.#O......OOO#....O.....O.
OO#..#.O.##..##..#........O..OO.......#..O.OO.OO..#O...OO.##
'''


def tilt_forward(grid: Grid) -> Grid:
    for j, col in grid.cols():
        curr = 0
        for i, ch in enumerate(col):
            match ch:
                case '#':
                    # cube-shaped
                    curr = i + 1
                case 'O':
                    # rounded and rolling
                    grid[i, j] = '.'
                    grid[curr, j] = 'O'
                    curr += 1

    return grid


def cycle(grid: Grid) -> Grid:
    for _ in 'NWSE':
        grid = tilt_forward(grid)
        grid.rotate_right()

    return grid


def beam_load(grid: Grid) -> int:
    return sum((grid.m - i) * row.count('O') for i, row in grid.rows())


part1 = beam_load(tilt_forward(grid.copy()))
part2 = 0

cycles = 1_000_000_000
prev = {}
for i in range(1, cycles + 1):
    grid = cycle(grid)

    key = hash(grid)
    if pi := prev.get(key):
        period = i - pi
        remaining = (cycles - i) % period
        for _ in range(remaining):
            grid = cycle(grid)

        part2 = beam_load(grid)
        break
    else:
        prev[key] = i

print(f'Part 1: {part1}')
print(f'Part 2: {part2}')
