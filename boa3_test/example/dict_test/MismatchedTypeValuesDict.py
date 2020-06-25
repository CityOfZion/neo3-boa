from typing import Dict, Sequence, Tuple


def Main() -> Sequence[int]:
    a: Dict[str, int] = {'one': 1, 'two': 2, 'three': 3}
    b: Tuple[int] = a.values()
    return b
