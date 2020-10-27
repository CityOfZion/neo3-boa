from typing import Tuple

from boa3.builtin import public


@public
def Main(a: Tuple[int]) -> int:
    return a[0]
