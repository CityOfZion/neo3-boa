from typing import Any, cast

from boa3.builtin import public
from boa3.builtin.type import UInt160


@public
def Main(value: Any) -> UInt160:
    x = cast(UInt160, value)
    return x
