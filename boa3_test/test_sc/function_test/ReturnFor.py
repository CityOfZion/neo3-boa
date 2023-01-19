from typing import List

from boa3.builtin.compile_time import public


@public
def Main(iterator: List[int]) -> int:
    for value in iterator:
        return value
    else:
        return 5
