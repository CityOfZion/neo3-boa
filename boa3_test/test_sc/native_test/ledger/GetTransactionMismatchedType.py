from boa3.sc.contracts import LedgerContract
from boa3.sc.types import Transaction


def main() -> Transaction:
    return LedgerContract.get_transaction(10)
