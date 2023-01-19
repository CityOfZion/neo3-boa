from typing import MutableSequence

from boa3.builtin.compile_time import public


@public
def clear_example() -> MutableSequence[int]:
    a: MutableSequence[int] = [1, 2, 3]
    MutableSequence.clear(a)
    return a
