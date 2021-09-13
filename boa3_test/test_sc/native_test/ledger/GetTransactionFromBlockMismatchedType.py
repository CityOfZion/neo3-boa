from boa3.builtin.interop.blockchain import Transaction
from boa3.builtin.nativecontract.ledger import Ledger


def main() -> Transaction:
    return Ledger.get_transaction_from_block('height', 'tx_index')
