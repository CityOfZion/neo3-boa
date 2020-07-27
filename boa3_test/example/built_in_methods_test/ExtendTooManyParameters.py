from typing import Any, List


def Main(op: str, args: list) -> List[Any]:
    a = [1, 2, 3]
    a.extend(4, 5, 6)
    return a
