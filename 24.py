#!/usr/bin/env python3
from lib import *

# 00:57
infile = sys.argv[1] if len(sys.argv)>1 else '24.in'
f = open(infile, 'r') if infile != '-' else sys.stdin

lines = list(map(Input, f))
'''
184964585341884, 113631924395348, 401845630841620 @ 61, 469,
331877282121819, 365938348079363, 314507465806130 @ 46, -106
263775277465044, 418701236136888, 52607746821705 @ 105, -170
208356602267478, 274354112299498, 294235176347885 @ 46, 8, -
215069209934964, 263266623283188, 304961521854129 @ -28, 48,
'''

class Hailstone:
    def __init__(self, xyz: list, d: list):
        # starting point
        self.xyz = np.array(xyz)
        # displacement per nanosecond (aka velocity)
        self.d = np.array(d)

    @property
    def xy(self):
        return self.xyz[:-1]

    @property
    def dxy(self):
        return self.d[:-1]


hailstones = []
for line in lines:
    xyz, d = line.split('@')
    xyz = map(int, xyz.split(','))
    d = map(int, d.split(','))
    hailstones.append(
        Hailstone(list(xyz), list(d))
    )


def count_test_area_intersections(hailstones: list):
    def time_of_intersection(a, b):
        # per https://cp-algorithms.com/geometry/basic-geometry.html#line-intersection
        return np.cross(b.xy - a.xy, b.dxy) / np.cross(a.dxy, b.dxy)

    cnt = 0
    # test_area_lowerbound = np.array([7]*2)
    # test_area_upperbound = np.array([27]*2)
    test_area_lowerbound = np.array([200000000000000]*2)
    test_area_upperbound = np.array([400000000000000]*2)
    for a, b in combinations(hailstones, 2):
        # no intersection if parallel
        if not np.cross(a.dxy, b.dxy):
            continue

        # at t1 'a' will intersect the path of 'b'
        t1 = time_of_intersection(a,b)
        intersection = a.xy + t1 * a.dxy

        within_test_area = np.all(
            np.logical_and(
                intersection >= test_area_lowerbound,
                intersection <= test_area_upperbound
            )
        )

        # count if the intersection is within test area AND happens after being thrown
        # (negative times are invalid)
        if within_test_area:
            # at t2 'b' will intersect the path of 'a'
            t2 = time_of_intersection(b,a)
            if t1 >= 0 and t2 >= 0:
                cnt += 1

    return cnt


def find_rock_xyz(hailstones: list):
    # for every hailstone, rock pos must be equal to hailstone pos at some time.
    # r0 + t*rd == h0 + t*hd

    # Rock
    (rx0, ry0, rz0) = z3.Ints('rx0 ry0 rz0')
    (rdx, rdy, rdz) = z3.Ints('rdx rdy rdz')

    solver = z3.Solver()
    for cnt, vec in enumerate(hailstones, 1):
        # hailstone
        (x0, y0, z0) = vec.xyz
        (dx, dy, dz) = vec.d
        # time of collision
        t = z3.Int(f't{cnt}')

        solver.add(
            rx0 + t * rdx == x0 + t * dx,
            ry0 + t * rdy == y0 + t * dy,
            rz0 + t * rdz == z0 + t * dz,
        )

        # The number of equations should meet the number of unknowns (9) in iteration 3.
        # (but maybe if there are redundant vectors we need more than 3?)
        #
        # unknowns in iteration 3:
        #  rx0 ry0 rz0
        #  rdx rdy rdz
        #  t1  t2  t3
        if cnt >= 3 and solver.check() == z3.sat:
            # we can solve the system.
            break
    else:
        raise RuntimeError('Could not solve system.')

    m = solver.model()
    return m[rx0].as_long(), m[ry0].as_long(), m[rz0].as_long()


part1 = count_test_area_intersections(hailstones)
part2 = sum(find_rock_xyz(hailstones))

print(f'Part 1: {part1}')
print(f'Part 2: {part2}')
