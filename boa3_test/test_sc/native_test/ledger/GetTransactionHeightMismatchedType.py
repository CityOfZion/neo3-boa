from boa3.sc.contracts import LedgerContract


def main() -> int:
    return LedgerContract.get_transaction_height(123)
