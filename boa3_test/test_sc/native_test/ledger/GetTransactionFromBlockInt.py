from boa3.sc.compiletime import public
from boa3.sc.contracts import LedgerContract
from boa3.sc.types import Transaction


@public
def main(height: int, tx_index: int) -> Transaction | None:
    return LedgerContract.get_transaction_from_block(height, tx_index)
