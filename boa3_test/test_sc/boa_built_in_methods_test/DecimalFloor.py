from boa3.sc.compiletime import public
from boa3.sc.math import floor


@public
def main(x: int, decimals: int) -> int:
    return floor(x, decimals)
