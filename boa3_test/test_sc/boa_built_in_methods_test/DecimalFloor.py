from boa3.builtin.compile_time import public
from boa3.builtin.math import floor


@public
def main(x: int, decimals: int) -> int:
    return floor(x, decimals)
