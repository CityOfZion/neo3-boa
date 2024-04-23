from typing import Any

from boa3.builtin.compile_time import public


@public
def Main(a: list[Any], pos: int, value: Any) -> list[Any]:
    a.insert(pos, value)
    return a
