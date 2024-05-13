from typing import Any, cast

from boa3.sc.compiletime import public
from boa3.sc.types import Transaction


@public
def get_transaction_hash(value: Any) -> bytes:
    tx = cast(Transaction, value)
    result = tx.hash
    return result
