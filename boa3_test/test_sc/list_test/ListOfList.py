from typing import List

from boa3.builtin import public


@public
def Main(a: List[List[int]]) -> int:
    return a[0][0]
