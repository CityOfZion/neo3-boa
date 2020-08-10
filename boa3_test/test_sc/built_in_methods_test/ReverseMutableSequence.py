from typing import MutableSequence


def Main() -> MutableSequence[int]:
    a: MutableSequence[int] = [1, 2, 3]
    a.reverse()
    return a
