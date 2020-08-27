from typing import List


def Main() -> List[int]:
    a: List[int] = [1, 2, 3]
    a.reverse(a)
    return a
