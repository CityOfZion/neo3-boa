from typing import Dict, Sequence


def Main() -> Sequence[int]:
    a: Dict[str, int] = {'one': 1, 'two': 2, 'three': 3}
    b = a.values()  # expected [1, 2, 3]
    return b
