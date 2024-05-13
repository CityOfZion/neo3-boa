from collections.abc import Sequence

from boa3.sc.compiletime import public


@public
def range_example(start: int, stop: int) -> Sequence:
    return range(start, stop)
