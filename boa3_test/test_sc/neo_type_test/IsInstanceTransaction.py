from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.interop.blockchain import Transaction, get_transaction
from boa3.builtin.type import UInt256


@public
def is_tx(value: Any) -> bool:
    return isinstance(value, Transaction)


@public
def get_transaction_is_tx(hash_: UInt256) -> bool:
    tx = get_transaction(hash_)
    return is_tx(tx)
