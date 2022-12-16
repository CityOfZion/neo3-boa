from typing import Tuple

from boa3.builtin.compile_time import public


@public
def Main() -> int:
    a: int = 0
    sequence: Tuple[int] = (3, 5, 15)

    for x in sequence:
        for y in sequence:
            a = a + x * y

    return a
