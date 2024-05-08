from typing import Any

from boa3.builtin.compile_time import public


@public
def Main() -> list[Any]:
    a: list[Any] = [1, 2, 3]
    a.append('4')
    return a
