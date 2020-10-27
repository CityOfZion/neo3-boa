from typing import MutableSequence

from boa3.builtin import public


@public
def Main() -> MutableSequence[int]:
    a: MutableSequence[int] = [1, 2, 3]
    a.extend([4, 5, 6])
    return a
