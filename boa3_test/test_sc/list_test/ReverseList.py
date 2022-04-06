from typing import List

from boa3.builtin import public


@public
def Main() -> List[int]:
    a: List[int] = [1, 2, 3]
    a.reverse()
    return a
