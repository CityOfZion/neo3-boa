from typing import List

from boa3.builtin.compile_time import public


@public
def Main() -> List[int]:
    x = add(1, 2, 3)
    y = add(5, 6)
    return [x, y]


def add(a: int, b: int, c: int = 0) -> int:
    return a + b + c
