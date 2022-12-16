from typing import Any, List

from boa3.builtin.compile_time import public


@public
def Main() -> List[Any]:
    a: List[Any] = [1, 2, 3]
    a.append('4')
    return a
