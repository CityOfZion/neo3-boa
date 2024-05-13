from boa3.sc.compiletime import public
from boa3.sc.math import sqrt


@public
def main(x: int) -> int:
    return sqrt(x)
