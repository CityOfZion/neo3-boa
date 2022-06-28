from boa3.builtin.interop.blockchain import get_transaction_signers


def main() -> list:
    return get_transaction_signers(123)
