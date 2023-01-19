from typing import Tuple

from boa3.builtin.compile_time import public


@public
def Main(items1: Tuple[int]) -> int:
    items2 = ('a', 'b', 'c', 'd'); value = items1[0]; count = value + len(items2)
    return count
