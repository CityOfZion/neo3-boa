from boa3.builtin.nativecontract.ledger import Ledger


def main() -> list:
    return Ledger.get_transaction_signers(123)
