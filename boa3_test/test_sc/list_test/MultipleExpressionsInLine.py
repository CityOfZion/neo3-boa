from typing import List

from boa3.builtin.compile_time import public


@public
def Main(items1: List[int]) -> int:
    items2 = [False, '1', 2, 3, '4']; value = items1[0]; count = value + len(items2)
    return count
