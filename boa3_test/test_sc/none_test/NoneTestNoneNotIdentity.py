from typing import Any

from boa3.sc.compiletime import public


@public
def Main(a: Any) -> bool:
    return a is not None
