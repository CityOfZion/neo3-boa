from typing import Any, cast

from boa3.sc.compiletime import public
from boa3.sc.types import Transaction


@public
def Main(value: Any) -> Transaction:
    x = cast(Transaction, value)
    return x
