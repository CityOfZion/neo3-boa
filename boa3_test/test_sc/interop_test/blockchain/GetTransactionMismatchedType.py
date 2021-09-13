from boa3.builtin.interop.blockchain import Transaction, get_transaction


def main() -> Transaction:
    return get_transaction(10)
