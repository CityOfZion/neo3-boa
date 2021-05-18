from typing import Any, cast

from boa3.builtin import public
from boa3.builtin.interop.blockchain import Transaction


@public
def Main(value: Any) -> Transaction:
    x = cast(Transaction, value)
    return x
