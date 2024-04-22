from typing import Any


def Main(op: str, args: list) -> list[Any]:
    a = [1, 2, 3]
    a.extend(4, 5, 6)
    return a
