from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.contracts import LedgerContract
from boa3.sc.types import UInt256, Transaction


@public
def is_tx(value: Any) -> bool:
    return isinstance(value, Transaction)


@public
def get_transaction_is_tx(hash_: UInt256) -> bool:
    tx = LedgerContract.get_transaction(hash_)
    return is_tx(tx)
