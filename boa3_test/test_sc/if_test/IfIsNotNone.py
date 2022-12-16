from typing import Union

from boa3.builtin.compile_time import public


@public
def main(a: Union[int, None]) -> bool:
    if a is not None:
        return some_function(a)
    else:
        return False


def some_function(var: int) -> bool:
    return True
