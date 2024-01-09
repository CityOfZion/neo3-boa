from typing import Any

from boa3.builtin.compile_time import public


@public
def Main(a: Any) -> bool:
    return a is not None
