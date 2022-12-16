from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.type import ECPoint


@public
def is_ecpoint(value: Any) -> bool:
    return isinstance(value, ECPoint)
