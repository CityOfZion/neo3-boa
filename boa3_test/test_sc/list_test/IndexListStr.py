from typing import List

from boa3.builtin.compile_time import public


@public
def main(a: List[str], value: str) -> int:
    return a.index(value)
