from typing import List

from boa3.builtin.compile_time import public


@public
def main() -> List[int]:
    m = [16, 2, 3, 4]
    m.pop(1)
    return m
