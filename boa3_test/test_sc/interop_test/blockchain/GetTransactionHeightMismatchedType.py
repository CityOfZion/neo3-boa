from boa3.builtin.interop.blockchain import get_transaction_height


def main() -> int:
    return get_transaction_height(123)
