from typing import Any

from boa3.builtin import public


@public
def Main(a: Any) -> bool:
    return a is None
