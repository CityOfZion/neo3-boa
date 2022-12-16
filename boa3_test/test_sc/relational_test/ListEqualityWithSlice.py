from typing import List

from boa3.builtin.compile_time import public


@public
def main(a: List[str], b: str) -> bool:
    return a[0] == b
