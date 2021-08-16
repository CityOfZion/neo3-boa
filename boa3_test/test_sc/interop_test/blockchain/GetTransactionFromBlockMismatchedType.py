from boa3.builtin.interop.blockchain import Transaction, get_transaction_from_block


def main() -> Transaction:
    return get_transaction_from_block('height', 'tx_index')
