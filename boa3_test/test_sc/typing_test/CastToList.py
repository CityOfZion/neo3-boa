from typing import Any, cast

from boa3.sc.compiletime import public


@public
def Main(value: Any) -> list[Any]:
    x = cast(list, value)
    return x
