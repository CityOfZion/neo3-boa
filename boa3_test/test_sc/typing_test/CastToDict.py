from typing import Any, cast

from boa3.builtin.compile_time import public


@public
def Main(value: Any) -> dict[Any, Any]:
    x = cast(dict, value)
    return x
