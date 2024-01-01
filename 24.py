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

@dataclasses.dataclass
class Line:
    xyz: np.ndarray
    d: np.ndarray

    @property
    def xy(self):
        return self.xyz[:-1]

    @property
    def dxy(self):
        return self.d[:-1]

vectors = []
for line in lines:
    xyz, dxyz = line.split('@')
    xyz = map(int, xyz.split(', '))
    dxyz = map(int, dxyz.split(', '))
    vectors.append(
        Line(np.array(list(xyz)), np.array(list(dxyz)))
    )

def count_test_area_intersections():
    def time_of_intersection(a, b):
        return np.cross(b.xy - a.xy, b.dxy) / np.cross(a.dxy, b.dxy)

    # test_area_lowerbound = np.array([7]*2)
    # test_area_upperbound = np.array([27]*2)
    test_area_lowerbound = np.array([200000000000000]*2)
    test_area_upperbound = np.array([400000000000000]*2)
    cnt = 0
    for a, b in combinations(vectors, 2):
        if not np.cross(a.dxy, b.dxy):
            continue

        intersection = a.xy + time_of_intersection(a,b) * a.dxy
        # print(a, b, intersection)
        if np.all(
            np.logical_and(
                intersection >= test_area_lowerbound,
                intersection <= test_area_upperbound
            )
        ):
            # if np.linalg.norm(intersection - (a.xy + a.dxy)) < np.linalg.norm(intersection - a.xy):
            # if (is_between(a.xy, (a.xy+a.dxy), intersection) and is_between(b.xy, (b.xy+b.dxy), intersection)) or np.all(a.xy == intersection) or np.all(b.xy == intersection):
            if time_of_intersection(a,b) >= 0 and time_of_intersection(b, a) >= 0:
                cnt += 1
                # print('yes', time_of_intersection(a,b), time_of_intersection(b, a))
    return cnt

def find_rock_xyz(vectors):
    # r = rock
    # r0 + t*rd = p0 + t*pd
    rx0, ry0, rz0 = z3.Ints('rx0 ry0 rz0')
    rdx, rdy, rdz = z3.Ints('rdx rdy rdz')
    solver = z3.Solver()
    for cnt, vec in enumerate(vectors, 1):
        (x0, y0, z0) = vec.xyz
        (dx, dy, dz) = vec.d
        t = z3.Int(f't{cnt}')
        solver.add(
            rx0 + t * rdx == x0 + t * dx,
            ry0 + t * rdy == y0 + t * dy,
            rz0 + t * rdz == z0 + t * dz,
        )

        if cnt >= 3 and solver.check() == z3.sat:
            # we can solve the system.
            # The number of equations should meet the number of unknowns (9) in iteration 3.
            # unknowns in iteration 3:
            # rx0 ry0 rz0
            # rdx rdy rdz
            # t1 t2 t3
            break

    m = solver.model()
    return m[rx0].as_long() + m[ry0].as_long() + m[rz0].as_long()

part1 = count_test_area_intersections()

'''
If we have a plane that slices all vectors, we would want to slide it until all
points cut on the plane align in 2-dimensions? Alternatively, if we can find two different
valid planes, then their intersection is the line we seek.

Ok, after staring at desmos, I think we can make planes like:
    pick vectors a, b, c
    use (a.xyz - b.xyz) and (c.xyz - b.xyz) for lines defining the plane
    make all planes with this sliding window of 3. intersecting

We could reframe this as:
    Find a configuration of (t, vector_id) pairs where we hit all
    vectors and maintain direction.
Some configuration of times t0, t1, ... , tn that when their corresponding
vector is taken at that time, the points hold constant slope, forming a line.
Aka the cross-product of points formed from this time configuration is 0.

Alright, we didn't get far with this. z3 system of equations time.
'''
part2 = find_rock_xyz(vectors)

print(f'Part 1: {part1}')
print(f'Part 2: {part2}')
