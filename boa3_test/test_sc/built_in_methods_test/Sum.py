from typing import List

from boa3.builtin import public


@public
def main(x: List[int]) -> int:
    return sum(x)
