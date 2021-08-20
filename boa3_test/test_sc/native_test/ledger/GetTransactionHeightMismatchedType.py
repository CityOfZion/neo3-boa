from boa3.builtin.nativecontract.ledger import Ledger


def main() -> int:
    return Ledger.get_transaction_height(123)
