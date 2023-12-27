from collections.abc import Sequence, Iterable, Iterator, Callable
from typing import Any, LiteralString, Self
from functools import cache
import sys, math, re, functools, operator, itertools, bisect, heapq
import numpy as np
from numpy.polynomial import Polynomial
import portion as P
from collections import defaultdict, deque, Counter, namedtuple
from sortedcontainers import *
import dataclasses
from itertools import (
    accumulate,
    chain,
    pairwise,
    cycle,
    product,
    combinations,
    groupby,
    repeat,
)
from more_itertools import sliding_window
from functools import cache, reduce
from extype import extension, extend_type_with


class ComplexExt(complex):
    # @extension
    # def __lt__(self, other):
    #     return self.real < other.real
    @extension
    @property
    def x(self):
        return self.real
    j = x

    @extension
    @property
    def xi(self):
        return int(self.real)

    @extension
    @property
    def y(self):
        return self.imag
    i = y

    @extension
    @property
    def yi(self):
        return int(self.imag)

    @extension
    @property
    def xy(self):
        return self.real, self.imag

    @extension
    @property
    def xyi(self):
        return int(self.real), int(self.imag)

    @extension
    def __mod__(self, other):
        if isinstance(other, tuple):
            return complex(self.real % other[0], self.imag % other[1])
        elif isinstance(other, (int, float)):
            return complex(self.real % other, self.imag % other)
        elif isinstance(other, complex):
            return complex(self.real % other.real, self.imag % other.imag)

    @extension
    def __imod__(self, other):
        return self.__mod__(other)


extend_type_with(complex, ComplexExt)

@dataclasses.dataclass
class Range3D:
    x: P.Interval
    y: P.Interval
    z: P.Interval
Point3D = namedtuple("Point3D", ['x', 'y', 'z'])

@dataclasses.dataclass
class Range2D:
    x: P.Interval
    y: P.Interval
Line = namedtuple("Line", ["s", "e"])

_dirs8 = [
    (di, dj)
    for di, dj in itertools.product((-1, 0, 1), (-1, 0, 1))
    if (di, dj) != (0, 0)
]

C = complex


def neighbors8(i: int, j: int, m: int, n: int):
    for di, dj in _dirs8:
        ni, nj = i + di, j + dj
        if 0 <= ni < m and 0 <= nj < n:
            yield ni, nj


def neighbors4(i: int, j: int, m: int, n: int) -> list[tuple[int, int]]:
    return [
        (ni, nj)
        for (ni, nj) in ((i - 1, j), (i, j + 1), (i + 1, j), (i, j - 1))
        if 0 <= ni < m and 0 <= nj < n
    ]


def get_ints(s: str, negatives: bool = False) -> list[int]:
    if negatives:
        return list(map(int, re.findall(r"-?\d+", s)))
    return list(map(int, re.findall(r"\d+", s)))


def ringwise(arr: list, i: int, j: int | None = None):
    if j is None:
        j = i
    return zip(arr[i::-1], arr[j:])


# until python 3.12 becomes default on homebrew.
def batched(iterable, n):
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(itertools.islice(it, n)):
        yield batch


def argsort(seq: Sequence, key: Callable = None, reverse: bool = False) -> list[int]:
    return sorted(
        range(len(seq)),
        key=(lambda i: key(seq[i])) if key else seq.__getitem__,
        reverse=reverse,
    )


def argmax(seq: Sequence, key: Callable = None) -> int:
    if key:
        key = lambda i: key(seq[i])
    else:
        key = seq.__getitem__

    return max(range(len(seq)), key=key)


def argmaxes(seq: Sequence, key: Callable = None) -> Iterable:
    N = len(seq)
    if key:
        seq = map(key, seq)

    seq = map(operator.neg, seq)
    max_heap = list(zip(seq, range(N)))
    heapq.heapify(max_heap)

    while max_heap:
        yield heapq.heappop(max_heap)[1]


def tokenize(s: str, delims: Iterable[str]) -> list[str]:
    # replace non-candidates with whitespace, then split.
    tr = str.maketrans(dict.fromkeys(delims, " "))
    return s.translate(tr).split()


def drop(s: str, chrs: str) -> str:
    trans = Input.make_tr("", "", chrs)
    return s.translate(trans)


def all_in(s: str, chrs: str) -> bool:
    return not drop(s, chrs)


class Input(str):
    def __new__(cls, content):
        return super().__new__(cls, content.rstrip())

    @staticmethod
    @cache
    def make_tr(from_chrs: str, to_chrs: str, kill_chrs: str):
        if len(from_chrs) == len(to_chrs):
            return str.maketrans(from_chrs, to_chrs, kill_chrs)
        else:
            return str.maketrans(dict.fromkeys(from_chrs, to_chrs[0]))

    def tr(self, from_chrs: str, to_chrs: str = "", kill_chrs: str = "") -> str:
        trans = Input.make_tr(from_chrs, to_chrs, kill_chrs)
        return self.translate(trans)

    def drop(self, chrs: str) -> str:
        trans = Input.make_tr("", "", chrs)
        return self.translate(trans)

    def tokenize(self, delims: Iterable[str]) -> list[str]:
        trans = Input.make_tr(delims, " ", "")
        return self.translate(trans).split()

    def partition_any(
        self, delims: Iterable[str], label: str = " "
    ) -> tuple[str, str, str]:
        trans = Input.make_tr(delims, label, "")
        delim_idx = self.translate(trans).find(label)
        return self[:delim_idx], self[delim_idx], self[delim_idx + 1 :]

    def to_int(self) -> int:
        return int(self)

    def to_digits(self) -> tuple[int, ...]:
        return tuple(map(int, self))


class Cardinal:
    N = U = 1
    S = D = 2
    W = L = 4
    E = R = 8
    ALL = N | W | S | E
    NULL = 0

    @staticmethod
    def neighbors(
        i: int, j: int, m: int = sys.maxsize, n: int = sys.maxsize, dirs: int = ALL
    ):
        if dirs & Cardinal.N and i - 1 >= 0:
            yield i - 1, j
        if dirs & Cardinal.W and j - 1 >= 0:
            yield i, j - 1
        if dirs & Cardinal.S and i + 1 < m:
            yield i + 1, j
        if dirs & Cardinal.E and j + 1 < n:
            yield i, j + 1


class ComplexCardinal(complex):
    N = U = +0 - 1j
    S = D = +0 + 1j
    W = L = -1 + 0j
    E = R = +1 + 0j
    FOUR_DIRECTIONS = (U, D, L, R)
    ROTATE_LEFT = -1j
    ROTATE_RIGHT = 1j
    # to rotate "left", multiply by -1j
    # to rotate "right", multiply by 1j
    # this is opposite bc North and South are flipped.

def zmanhattan(a: complex, b: complex = 0) -> int:
    dz = a - b
    return abs(int(dz.real)) + abs(int(dz.imag))

class PriorityQueue(list):
    def __init__(self, data=[]):
        super().__init__()
        self.counter = itertools.count()
        for item in data:
            self.push(item)

    def push(self, _item):
        if len(_item) <= 1:
            heapq.heappush(self, _item)
        else:
            item = [_item[0], next(self.counter), *_item[1:]]
            heapq.heappush(self, item)

    def pop(self):
        item = heapq.heappop(self)
        item.pop(1)
        return item


def dump_zgrid(grid: dict, m: int, n: int):
    row = []
    for j, loc in enumerate(sorted(grid.keys(), key=lambda z: (z.imag, z.real)), 1):
        row.append(grid[loc])
        if j % n == 0:
            print("".join(map(str, row)))
            row.clear()
    print()


class ZGrid(dict[complex, Any]):
    def __init__(self, data: dict[complex, Any], m: int = -1, n: int = -1):
        super().__init__(data)

        if m == n == -1:
            self.mnm, self.mnn, self.mxm, self.mxn = self.bounding_box()
            self.m = self.mxm + 1 - self.mnm
            self.n = self.mxn + 1 - self.mnn
        else:
            self.mnm = 0
            self.mxm = m - 1
            self.m = m
            self.mnn = 0
            self.mxn = n - 1
            self.n = n

    def bounding_box(self) -> tuple[int, int, int, int]:
        min_c = min_r = sys.maxsize
        max_c = max_r = ~sys.maxsize
        for key in self:
            c, r = key.xyi
            min_c = min(min_c, c)
            max_c = max(max_c, c)
            min_r = min(min_r, r)
            max_r = max(max_r, r)

        return min_r, min_c, max_r, max_c

    @classmethod
    def from_text(cls, text: str):
        lines = text.splitlines()
        return cls(
            {
                complex(x, y): ch
                for y, line in enumerate(lines)
                for x, ch in enumerate(line)
            },
            len(lines),
            len(lines[0]),
        )

    @classmethod
    def from_text_with_drop(cls, text: str, drop_chs: str):
        lines = text.splitlines()
        return cls(
            {
                complex(x, y): ch
                for y, line in enumerate(lines)
                for x, ch in enumerate(line)
                if ch not in drop_chs
            },
            len(lines),
            len(lines[0]),
        )

    @classmethod
    def from_text_with_transform(cls, text: str, transform: Callable):
        lines = text.splitlines()
        return cls(
            {
                complex(x, y): transform(ch)
                for y, line in enumerate(lines)
                for x, ch in enumerate(line)
            },
            len(lines),
            len(lines[0]),
        )

    def set_all(self, locs: Iterable[complex], value: Any):
        for loc in locs:
            self[loc] = value

    def all(self):
        for j, loc in enumerate(sorted(self.keys(), key=lambda z: (z.imag, z.real)), 1):
            yield self[loc]

    def locs(self):
        yield from sorted(self.keys(), key=lambda z: (z.imag, z.real))

    def find(self, v):
        return next((loc for loc in self.locs() if self[loc] == v), None)

    def rows(self):
        row = []
        for j, loc in enumerate(sorted(self.keys(), key=lambda z: (z.imag, z.real)), 1):
            row.append(self[loc])
            if j % self.n == 0:
                yield row
                row.clear()

    def filled_rows(self, fill_ch: str):
        for i in range(self.mnm, self.mxm + 1):
            row = []
            for j in range(self.mnn, self.mxn + 1):
                row.append(self.get(complex(j, i), fill_ch))
            yield row

    def print(self, fill_ch=" "):
        for row in self.filled_rows(fill_ch):
            print("".join(map(str, row)))

        print()
        # for j, loc in enumerate(sorted(self.keys(), key=lambda z: (z.imag, z.real)), 1):
        #     row.append(self[loc])
        #     if j % self.n == 0:
        #         print(''.join(map(str, row)))
        #         row.clear()
        # print()

    def compress(self):
        # map to relative coordinates and store actual elsewhere
        pass


class Grid(list):
    """
    from_text()
    cols()
    for row in grid:
    .values()
    .where -> [(i,j, v)]
    """

    def __init__(self, data):
        super().__init__(data)
        self.m = len(self)
        self.n = len(self[0])

    def __getitem__(self, loc):
        if isinstance(loc, tuple):
            i, j = loc
            return super().__getitem__(i)[j]
        elif isinstance(loc, complex):
            i, j = int(loc.imag), int(loc.real)
            return super().__getitem__(i)[j]
        else:
            return super().__getitem__(loc)

    def __setitem__(self, loc, value):
        if isinstance(loc, tuple):
            i, j = loc
            super().__getitem__(i)[j] = value
        elif isinstance(loc, complex):
            i, j = int(loc.imag), int(loc.real)
            super().__getitem__(i)[j] = value
        else:
            super().__setitem__(loc, value)

    def copy(self) -> Self:
        return type(self)(row[:] for row in self)

    def get(self, loc):
        if isinstance(loc, tuple):
            if (0 <= loc[0] < self.m) and (0 <= loc[1] < self.n):
                return self[loc]
        elif isinstance(loc, complex):
            if (0 <= loc.imag < self.m) and (0 <= loc.real < self.n):
                return self[int(loc.imag), int(loc.real)]
        return None

    @classmethod
    def from_text(cls, text: str):
        return cls([list(line) for line in text.splitlines()])

    def cols(self):
        return enumerate(zip(*self))

    def rows(self):
        return enumerate(self)

    def keys(self):
        m, n = self.m, self.n
        for i in range(m):
            for j in range(n):
                yield i, j

    def values(self):
        for row in self:
            for val in row:
                yield val

    def items(self):
        for i, row in enumerate(self):
            for j, val in enumerate(row):
                yield i, j, val

    def where(self, target):
        for i, row in enumerate(self):
            for j, val in enumerate(row):
                if val == target:
                    yield i, j

    def first(self, target):
        for i, row in enumerate(self):
            for j, val in enumerate(row):
                if val == target:
                    return i, j

        return None

    find = first

    def print(self):
        for row in self:
            print("".join(map(str, row)))
        print()

    def rotate_left(self):
        new_grid = [list(col) for _, col in self.cols()]
        self.clear()
        self.extend(reversed(new_grid))
        self.m = len(self)
        self.n = len(self[0])

    def rotate_right(self):
        new_grid = [list(reversed(col)) for _, col in self.cols()]
        self.clear()
        self.extend(new_grid)
        self.m = len(self)
        self.n = len(self[0])

    def to_tuple(self):
        return tuple(map(tuple, self))

    def __str__(self):
        return "\n".join("".join(map(str, row)) for row in self)

    def __hash__(self):
        return hash(self.to_tuple())


def sort2(a, b):
    if a <= b:
        return a, b
    else:
        return b, a


def zsort2(a: complex, b: complex):
    if (a.imag, a.real) <= (b.imag, b.real):
        return a, b
    else:
        return b, a

def IntervalMultiDict(dicts: list[dict[P.Interval, Any]], how: Callable = set.union):
    '''
    Substantially faster than doing P.IntervalDict.combine repeatedly.
    Portion definitely needs an IntervalMultiDict type.
    '''
    def combine(ivds: list[dict[P.Interval, Any]]):
        match len(ivds):
            case 0:
                return P.IntervalDict()
            case 1:
                return P.IntervalDict(ivds[0])
            case cnt:
                return P.IntervalDict.combine(
                    combine(ivds[:cnt//2]),
                    combine(ivds[cnt//2:]),
                    how=how
                )

    return combine(dicts)
