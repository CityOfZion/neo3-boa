from typing import Tuple

from boa3.builtin import public


@public
def main(value: int, some_tuple: Tuple[int]) -> bool:
    return value in some_tuple
