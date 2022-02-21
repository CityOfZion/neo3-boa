from boa3.builtin import public
from boa3.builtin.math import ceil


@public
def main(x: int, decimals: int) -> int:
    return ceil(x, decimals)
