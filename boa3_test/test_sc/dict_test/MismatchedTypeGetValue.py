from typing import Dict


def Main(a: Dict[str, int]) -> int:
    return a[0]  # raises runtime error if the dict doesn't contain this key
