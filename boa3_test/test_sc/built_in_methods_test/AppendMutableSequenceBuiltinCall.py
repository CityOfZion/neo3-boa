from collections.abc import MutableSequence

from boa3.sc.compiletime import public


@public
def append_example() -> MutableSequence[int]:
    a: MutableSequence[int] = [1, 2, 3]
    MutableSequence.append(a, 4)
    return a
