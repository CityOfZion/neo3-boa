from typing import Any, cast

from boa3.builtin.compile_time import public


@public
def Main(value: Any) -> list[Any]:
    x = cast(list, value)
    return x
