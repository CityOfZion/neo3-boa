from boa3.builtin import public
from boa3.builtin.interop.blockchain import Transaction


@public
def main() -> Transaction:
    return Transaction()
