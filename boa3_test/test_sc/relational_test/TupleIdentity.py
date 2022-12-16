from typing import Tuple

from boa3.builtin.compile_time import public


@public
def with_attribution() -> bool:
    a: Tuple[int, int, int] = (1, 2, 3)
    b = a
    return a is b


@public
def without_attribution() -> bool:
    a: Tuple[int, int, int] = (1, 2, 3)
    b: Tuple[int, int, int] = (1, 2, 3)
    return a is b
