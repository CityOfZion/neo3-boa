from typing import Sequence

from boa3.builtin.compile_time import public


@public
def range_example(start: int, stop: int) -> Sequence:
    return range(start, stop)
