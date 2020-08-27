from typing import Any, List


def Main(op: str, args: list) -> List[Any]:
    a: List[Any] = [1, 2, 3]
    a.extend(('4', 5, True))
    return a  # expected [1, 2, 3, '4', 5, True]
