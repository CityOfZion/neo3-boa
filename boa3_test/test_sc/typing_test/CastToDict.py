from typing import Any, cast

from boa3.sc.compiletime import public


@public
def Main(value: Any) -> dict[Any, Any]:
    x = cast(dict, value)
    return x
