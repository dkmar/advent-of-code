import heapq
import itertools
import operator
import re
from collections.abc import Sequence, Iterable
from typing import LiteralString
from functools import cache

dirs = [(di, dj) for di, dj in itertools.product((-1, 0, 1), (-1, 0, 1))
        if (di, dj) != (0, 0)]


def neighbors8(i: int, j: int, m: int, n: int):
    for di, dj in dirs:
        ni, nj = i + di, j + dj
        if 0 <= ni < m and 0 <= nj < n:
            yield ni, nj


def neighbors(i: int, j: int, m: int, n: int) -> list[tuple[int, int]]:
    return [(ni, nj) for (ni, nj)
            in ((i - 1, j), (i, j + 1), (i + 1, j), (i, j - 1))
            if 0 <= ni < m and 0 <= nj < n]


def get_ints(s: str, negatives: bool = False) -> list[int]:
    if negatives:
        return list(map(int, re.findall(r'-?\d+', s)))
    return list(map(int, re.findall(r'\d+', s)))


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

    def to_int(self) -> int:
        return int(self)

    def to_digits(self) -> tuple[int, ...]:
        return tuple(map(int, self))

