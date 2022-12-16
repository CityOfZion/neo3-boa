from typing import MutableSequence

from boa3.builtin.compile_time import public


@public
def Main() -> MutableSequence[int]:
    a: MutableSequence[int] = [1, 2, 3]
    a.reverse()
    return a
