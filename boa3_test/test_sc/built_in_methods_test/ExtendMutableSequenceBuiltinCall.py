from collections.abc import MutableSequence

from boa3.sc.compiletime import public


@public
def Main() -> MutableSequence[int]:
    a: MutableSequence[int] = [1, 2, 3]
    MutableSequence.extend(a, [4, 5, 6])
    return a
