from typing import List

from boa3.builtin import public


@public
def Main(a: List[int], value: int) -> List[int]:
    a.remove(value)
    return a
