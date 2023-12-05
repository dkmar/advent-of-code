import itertools

dirs = [(di, dj) for di, dj in itertools.product((-1,0,1), (-1,0,1))
        if (di, dj) != (0, 0)]

def neighbors8(i:int, j:int, m:int, n:int):
    for di, dj in dirs:
        ni, nj = i+di, j+dj
        if 0<=ni<m and 0<=nj<n:
            yield ni, nj


def neighbors(i:int, j:int, m:int, n:int) -> list[tuple[int,int]]:
    return [(ni,nj) for (ni,nj) 
                in ((i-1,j),(i,j+1),(i+1,j),(i,j-1))
                if 0<=ni<m and 0<=nj<n]

import re
def get_ints(s:str, negatives:bool=False) -> list[int]:
    if negatives:
        return list(map(int, re.findall(r'-?\d+', s)))
    return list(map(int, re.findall(r'\d+', s)))