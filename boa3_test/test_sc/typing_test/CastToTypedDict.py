from typing import Any, Dict, cast

from boa3.builtin.compile_time import public


@public
def Main(value: Any) -> int:
    x = cast(Dict[str, int], value)
    return x['example']
