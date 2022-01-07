from boa3.builtin import public
from boa3.builtin.math import floor


@public
def main(x: int, decimals: int) -> int:
    return floor(x, decimals)
