from typing import List

from boa3.builtin.compile_time import public


@public
def Main(a: List[int]) -> list:
    a[0] = 1
    return a
