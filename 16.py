#!/usr/bin/env python3
from lib import *

# 23:18
infile = sys.argv[1] if len(sys.argv)>1 else '16.in'
f = open(infile, 'r') if infile != '-' else sys.stdin

'''
\\.........../..............-..../....\.......\.............
................................../.......|..\..........-...
.............................|...|.............\..\.....|...
\................\.............|..../........\\.....\\......
......\..............|...|..../........-../.................

empty space .
mirrors     / \
splitters   | -
beam enters at 0,0 going right
want: # of coords touched by beam.
'''
grid = ZGrid.from_text(f.read().rstrip())
UP, DOWN, LEFT, RIGHT = ComplexCardinal.FOUR_DIRECTIONS

def beam_redirection(direction: complex, ch: str):
    match ch:
        case '/':
            # reflect left if horizontal; right if vertical
            yield (direction * -1j) if direction.real else (direction * 1j)
        case '\\':
            # reflect left if vertical; right if horizontal
            yield (direction * -1j) if direction.imag else (direction * 1j)
        case '|' if direction.real:
            # split if horizontal
            yield UP
            yield DOWN
        case '-' if direction.imag:
            # split if vertical
            yield LEFT
            yield RIGHT
        case _:
            # in-line with '-' or '|'. keep going.
            yield direction

def trace_beam(loc: complex, direction: complex, tiles: set) -> complex | None:
    # walk (and track) tiles until we reach an obstacle or boundary
    while True:
        loc += direction
        ch = grid.get(loc, None)
        if ch is None:
            return None

        tiles.add(loc)
        if ch != '.':
            return loc

def tiles_energized(start: complex, direction: complex) -> int:
    tiles = set()
    seen = set()
    beams = {(start, direction)}
    while beams:
        next_beams = set()
        for loc, direction in beams:
            # walk beam until collision
            endpoint = trace_beam(loc, direction, tiles)
            if endpoint is None:
                # out-of-bounds
                continue
            # gather resulting beams
            for new_direction in beam_redirection(direction, grid[endpoint]):
                next_beams.add((endpoint, new_direction))

        # update frontier and seen-set
        beams = next_beams - seen
        seen |= beams

    return len(tiles)

part1 = tiles_energized(-1+0j, RIGHT)
part2 = max(
    max(tiles_energized(complex(-1, i), RIGHT) for i in range(grid.m)),
    max(tiles_energized(complex(grid.n, i), LEFT) for i in range(grid.m)),
    max(tiles_energized(complex(j, -1), DOWN) for j in range(grid.n)),
    max(tiles_energized(complex(j, grid.m), UP) for j in range(grid.n)),
)
print(f'Part 1: {part1}')
print(f'Part 2: {part2}')
