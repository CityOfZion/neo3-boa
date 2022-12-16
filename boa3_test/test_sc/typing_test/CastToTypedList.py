from typing import Any, List, cast

from boa3.builtin.compile_time import public


@public
def Main(value: Any) -> int:
    x = cast(List[int], value)
    return x[0]
