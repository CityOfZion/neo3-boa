from typing import List

from boa3.builtin import public


def return_none(a: List[int]) -> None:
    a.append(10)
    return None


@public
def main() -> List[int]:
    a = [2, 4, 6, 8]
    return_none(a)
    return a
