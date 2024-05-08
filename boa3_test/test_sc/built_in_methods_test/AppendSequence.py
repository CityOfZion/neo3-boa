from collections.abc import Sequence
from typing import Any


def Main(op: str, args: list) -> Sequence[int]:
    a: Sequence[Any] = (1, 2, 3)
    a.append(4)  # compiler error - only mutable sequence can append new values
    return a
