from typing import List

from boa3.builtin import public


@public
def Main(iterator: List[int]) -> int:
    x = 0
    for value in iterator:
        x += value
    else:
        return x
