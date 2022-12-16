from typing import List

from boa3.builtin.compile_time import public


@public
def Main(op: str, args: list) -> List[int]:
    a = [1, 2, 3]
    a.clear()
    return a
