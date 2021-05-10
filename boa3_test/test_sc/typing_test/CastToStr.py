from typing import Any, cast

from boa3.builtin import public


@public
def Main(value: Any) -> str:
    x = cast(str, value)
    return x
