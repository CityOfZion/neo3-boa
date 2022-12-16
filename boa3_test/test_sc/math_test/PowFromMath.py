from math import pow

from boa3.builtin.compile_time import public


@public
def main(x: int, y: int) -> int:
    return pow(x, y)
