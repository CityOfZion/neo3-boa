from typing import List


def Main(op: str, args: list) -> List[int]:
    a = [1, 2, 3]
    list.extend(a, [4, 5, 6])
    return a  # expected [1, 2, 3, 4, 5, 6]
