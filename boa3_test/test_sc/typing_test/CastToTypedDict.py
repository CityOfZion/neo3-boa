from typing import Any, cast

from boa3.sc.compiletime import public


@public
def Main(value: Any) -> int:
    x = cast(dict[str, int], value)
    return x['example']
