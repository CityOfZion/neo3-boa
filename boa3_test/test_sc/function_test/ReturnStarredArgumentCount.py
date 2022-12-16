from typing import List

from boa3.builtin.compile_time import public


@public
def fun_with_starred(*args: int) -> int:
    return len(args)


@public
def main(list_with_args: List[int]) -> int:
    return fun_with_starred(*list_with_args)
