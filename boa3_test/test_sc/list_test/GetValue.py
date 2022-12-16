from typing import List

from boa3.builtin.compile_time import public


@public
def Main(a: List[int]) -> int:
    return a[0]  # raises runtime error if the list is empty
