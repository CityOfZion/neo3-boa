from typing import Any, cast

from boa3.builtin.compile_time import public


@public
def Main(value: Any) -> int:
    x = cast(list[int], value)
    return x[0]
