from typing import Union

from boa3.builtin import public


@public
def main(a: Union[int, None]) -> bool:
    if a is None:
        return True
    else:
        return some_function(a)


def some_function(var: int) -> bool:
    return False
