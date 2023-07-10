from typing import Optional

from boa3.builtin.compile_time import public
from boa3.builtin.interop.blockchain import Transaction
from boa3.builtin.nativecontract.ledger import Ledger


@public
def main(height: int, tx_index: int) -> Optional[Transaction]:
    return Ledger.get_transaction_from_block(height, tx_index)
