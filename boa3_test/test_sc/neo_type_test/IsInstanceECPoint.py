from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.types import ECPoint


@public
def is_ecpoint(value: Any) -> bool:
    return isinstance(value, ECPoint)
