from typing import Tuple

from boa3.builtin import public


@public
def main(value: bytes, some_tuple: Tuple[str]) -> bool:
    return value in some_tuple
