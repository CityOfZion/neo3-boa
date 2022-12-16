from typing import List

from boa3.builtin.compile_time import public


@public
def main(a: List[int], value: int) -> int:
    var = return_same(a.index(value))

    return var


def return_same(arg: int) -> int:
    return arg
