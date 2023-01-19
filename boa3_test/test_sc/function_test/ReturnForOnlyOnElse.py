from typing import List

from boa3.builtin.compile_time import public


@public
def Main(iterator: List[int]) -> int:
    x = 0
    for value in iterator:
        x += value
    else:
        return x
