from collections.abc import Sequence, Iterable
from typing import Any, LiteralString, Self
from functools import cache
import sys, math, re, functools, operator, itertools, bisect, heapq
import numpy as np
from numpy.polynomial import Polynomial
import portion as P
from collections import defaultdict, deque, Counter
from itertools import accumulate, chain, pairwise, cycle, product, combinations, groupby, repeat
from more_itertools import sliding_window
from functools import cache, reduce

_dirs8 = [(di, dj) for di, dj in itertools.product((-1, 0, 1), (-1, 0, 1))
          if (di, dj) != (0, 0)]


def neighbors8(i: int, j: int, m: int, n: int):
    for di, dj in _dirs8:
        ni, nj = i + di, j + dj
        if 0 <= ni < m and 0 <= nj < n:
            yield ni, nj


def neighbors4(i: int, j: int, m: int, n: int) -> list[tuple[int, int]]:
    return [(ni, nj) for (ni, nj)
            in ((i - 1, j), (i, j + 1), (i + 1, j), (i, j - 1))
            if 0 <= ni < m and 0 <= nj < n]


def get_ints(s: str, negatives: bool = False) -> list[int]:
    if negatives:
        return list(map(int, re.findall(r'-?\d+', s)))
    return list(map(int, re.findall(r'\d+', s)))


def ringwise(arr: list, i: int, j: int | None = None):
    if j is None:
        j = i
    return zip(arr[i::-1], arr[j:])


# until python 3.12 becomes default on homebrew.
def batched(iterable, n):
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError('n must be at least one')
    it = iter(iterable)
    while batch := tuple(itertools.islice(it, n)):
        yield batch


def argsort(seq: Sequence, key: callable = None, reverse: bool = False) -> list[int]:
    return sorted(range(len(seq)),
                  key=(lambda i: key(seq[i])) if key else seq.__getitem__,
                  reverse=reverse)


def argmax(seq: Sequence, key: callable = None) -> int:
    if key:
        key = lambda i: key(seq[i])
    else:
        key = seq.__getitem__

    return max(range(len(seq)), key=key)


def argmaxes(seq: Sequence, key: callable = None) -> Iterable:
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
    tr = str.maketrans(dict.fromkeys(delims, ' '))
    return s.translate(tr).split()


def drop(s: str, chrs: str) -> str:
    trans = Input.make_tr('', '', chrs)
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

    def tr(self, from_chrs: str, to_chrs: str = '', kill_chrs: str = '') -> str:
        trans = Input.make_tr(from_chrs, to_chrs, kill_chrs)
        return self.translate(trans)

    def drop(self, chrs: str) -> str:
        trans = Input.make_tr('', '', chrs)
        return self.translate(trans)

    def tokenize(self, delims: Iterable[str]) -> list[str]:
        trans = Input.make_tr(delims, ' ', '')
        return self.translate(trans).split()

    def partition_any(self, delims: Iterable[str], label: str = ' ') -> tuple[str, str, str]:
        trans = Input.make_tr(delims, label, '')
        delim_idx = self.translate(trans).find(label)
        return self[:delim_idx], self[delim_idx], self[delim_idx+1:]

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
    def neighbors(i: int, j: int, m: int = sys.maxsize, n: int = sys.maxsize, dirs: int = ALL):
        if dirs & Cardinal.N and i - 1 >= 0:
            yield i - 1, j
        if dirs & Cardinal.W and j - 1 >= 0:
            yield i, j - 1
        if dirs & Cardinal.S and i + 1 < m:
            yield i + 1, j
        if dirs & Cardinal.E and j + 1 < n:
            yield i, j + 1

class ComplexCardinal:
    N = U = +0-1j
    S = D = +0+1j
    W = L = -1+0j
    E = R = +1+0j
    FOUR_DIRECTIONS = (U, D, L, R)
    ROTATE_LEFT = -1j
    ROTATE_RIGHT = 1j
    # to rotate "left", multiply by -1j
    # to rotate "right", multiply by 1j
    # this is opposite bc North and South are flipped.

class ZGrid(dict[complex, Any]):
    def __init__(self, data: dict[complex, Any], m: int, n: int):
        super().__init__(data)
        self.m = m
        self.n = n

    @classmethod
    def from_text(cls, text: str):
        lines = text.splitlines()
        return cls({
            complex(x,y): ch
            for y, line in enumerate(lines)
            for x, ch in enumerate(line)
        }, len(lines), len(lines[0]))

    def set_all(self, locs: Iterable[complex], value: Any):
        for loc in locs:
            self[loc] = value

    def print(self):
        row = []
        for j, loc in enumerate(sorted(self.keys(), key=lambda z: (z.imag, z.real)), 1):
            row.append(self[loc])
            if j % self.n == 0:
                print(''.join(map(str, row)))
                row.clear()
        print()

class Grid(list):
    '''
    from_text()
    cols()
    for row in grid:
    .values()
    .where -> [(i,j, v)]
    '''

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
            print(''.join(map(str, row)))
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
        return '\n'.join(''.join(map(str, row)) for row in self)

    def __hash__(self):
        return hash(self.to_tuple())




def sort2(a, b):
    if a <= b:
        return a, b
    else:
        return b, a
