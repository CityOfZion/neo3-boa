from typing import Tuple


def Main(op: str, args: list) -> Tuple[int]:
    a = (1, 2, 3)
    a.append(4)  # compiler error - cannot append values to a tuple
    return a
