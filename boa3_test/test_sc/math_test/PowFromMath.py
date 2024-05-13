from math import pow

from boa3.sc.compiletime import public


@public
def main(x: int, y: int) -> int:
    return pow(x, y)
