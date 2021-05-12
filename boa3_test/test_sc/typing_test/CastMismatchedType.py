from typing import Any, cast

from boa3.builtin import public


def Main(value: Any) -> int:
    x = cast(4, value)
    return x
