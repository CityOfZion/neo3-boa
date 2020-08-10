from typing import List


def Main(op: str, args: list) -> List[int]:
    a = [1, 2, 3]
    a.extend(('4', '5', '6'))
    return a
