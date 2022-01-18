from math import pow

from boa3.builtin import public


@public
def main(x: int, y: int) -> int:
    return pow(x, y)
