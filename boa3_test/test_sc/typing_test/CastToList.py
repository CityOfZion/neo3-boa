from typing import Any, List, cast

from boa3.builtin import public


@public
def Main(value: Any) -> List[Any]:
    x = cast(list, value)
    return x
