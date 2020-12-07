from typing import List

from boa3.builtin import public


@public
def main(a: List[str], b: str) -> bool:
    return a[0] == b
