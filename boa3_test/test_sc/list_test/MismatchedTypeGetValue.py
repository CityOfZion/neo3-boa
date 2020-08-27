from typing import List


def Main(a: List[int]) -> int:
    return a[0][0]  # expecting sequence[sequence[]], but receiver sequence[int]
