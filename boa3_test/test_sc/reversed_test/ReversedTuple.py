from typing import Tuple

from boa3.builtin import public


@public
def main(a: Tuple) -> reversed:
    return reversed(a)
