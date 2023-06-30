from typing import Optional

from boa3.builtin.compile_time import public
from boa3.builtin.interop.blockchain import Transaction
from boa3.builtin.nativecontract.ledger import Ledger
from boa3.builtin.type import UInt256


@public
def main(hash_: UInt256, tx_index: int) -> Optional[Transaction]:
    return Ledger.get_transaction_from_block(hash_, tx_index)
