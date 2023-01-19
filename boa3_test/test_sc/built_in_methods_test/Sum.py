from typing import List

from boa3.builtin.compile_time import public


@public
def main(x: List[int]) -> int:
    return sum(x)
