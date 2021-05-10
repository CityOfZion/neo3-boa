from typing import Any, Dict, cast

from boa3.builtin import public


@public
def Main(value: Any) -> int:
    x = cast(Dict[str, int], value)
    return x['example']
