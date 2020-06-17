from typing import List


def Main(op: str, args: list) -> List[int]:
    a = [1, 2, 3]
    list.append(a, [a])  # expecting int value to append
    return a
