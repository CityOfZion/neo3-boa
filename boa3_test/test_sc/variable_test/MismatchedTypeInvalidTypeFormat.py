# from typing import List

from boa3.builtin import public


@public
def Main(a: [int]) -> [int]:  # should be List[int] instead of [int]
    return a
