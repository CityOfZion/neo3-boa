from boa3.sc.compiletime import public
from boa3.sc.math import ceil


@public
def main(x: int, decimals: int) -> int:
    return ceil(x, decimals)
