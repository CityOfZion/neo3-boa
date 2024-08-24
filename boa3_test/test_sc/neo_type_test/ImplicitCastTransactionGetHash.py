from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.types import Transaction


@public
def get_transaction_hash(value: Any) -> bytes:
    tx: Transaction = value
    return tx.hash
