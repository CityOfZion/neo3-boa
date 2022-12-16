from typing import List

from boa3.builtin.compile_time import public


@public
def Main(a: List[int], value: int) -> List[int]:
    a.remove(value)
    return a
