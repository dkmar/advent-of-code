from typing import List,Tuple
def neighbors(i:int, j:int, m:int, n:int) -> List[Tuple[int,int]]:
    return [(ni,nj) for (ni,nj) 
                in ((i-1,j),(i,j+1),(i+1,j),(i,j-1))
                if 0<=ni<m and 0<=nj<n]

import re
def get_ints(s:str, negatives:bool=False) -> List[int]:
    if negatives:
        return list(map(int, re.findall(r'-?\d+', s)))
    return list(map(int, re.findall(r'\d+', s)))