from typing import List


def Main(a: List[int]) -> int:
    return a[-1]  # raises runtime error if the list is empty
