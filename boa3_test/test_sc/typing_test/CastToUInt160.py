from typing import Any, cast

from boa3.sc.compiletime import public
from boa3.sc.types import UInt160


@public
def Main(value: Any) -> UInt160:
    x = cast(UInt160, value)
    return x
