from typing import Any, cast

from boa3.builtin.compile_time import public
from boa3.builtin.interop.blockchain import Transaction


@public
def get_transaction_hash(value: Any) -> bytes:
    tx = cast(Transaction, value)
    return tx.hash
