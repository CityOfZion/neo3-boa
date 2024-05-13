from boa3.sc.contracts import LedgerContract
from boa3.sc.types import Transaction


def main() -> Transaction:
    return LedgerContract.get_transaction_from_block('height', 'tx_index')
