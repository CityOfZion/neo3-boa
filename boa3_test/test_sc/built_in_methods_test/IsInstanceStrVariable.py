from typing import Any

from boa3.sc.compiletime import public


@public
def Main(a: Any) -> bool:
    return isinstance(a, str)
