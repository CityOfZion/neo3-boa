from typing import Any, Sequence


def Main(op: str, args: list) -> Sequence[int]:
    a: Sequence[Any] = (1, 2, 3)
    a.extend([4, 5, 6])  # compiler error - only mutable sequence can append new values
    return a
