from typing import Dict


def Main(a: Dict[int, str]) -> str:
    return a[0]  # raises runtime error if the dict doesn't contain this key
