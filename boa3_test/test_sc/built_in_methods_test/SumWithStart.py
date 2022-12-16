from typing import List

from boa3.builtin.compile_time import public


@public
def main(x: List[int], start: int) -> int:
    return sum(x, start)
