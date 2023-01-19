# from typing import List

from boa3.builtin.compile_time import public


@public
def Main(a: [int]) -> [int]:  # should be List[int] instead of [int]
    return a
