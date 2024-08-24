from boa3.sc.contracts import LedgerContract


def main() -> list:
    return LedgerContract.get_transaction_signers(123)
