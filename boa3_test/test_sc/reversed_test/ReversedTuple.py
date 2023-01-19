from typing import Tuple

from boa3.builtin.compile_time import public


@public
def main(a: Tuple) -> reversed:
    return reversed(a)
