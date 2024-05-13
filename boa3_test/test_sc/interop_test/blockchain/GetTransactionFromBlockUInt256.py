from boa3.sc.compiletime import public
from boa3.sc.contracts import LedgerContract
from boa3.sc.types import UInt256, Transaction


@public
def main(hash_: UInt256, tx_index: int) -> Transaction | None:
    return LedgerContract.get_transaction_from_block(hash_, tx_index)
