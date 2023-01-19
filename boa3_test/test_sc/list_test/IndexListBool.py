from typing import List

from boa3.builtin.compile_time import public


@public
def main(a: List[bool], value: bool) -> int:
    return a.index(value)
