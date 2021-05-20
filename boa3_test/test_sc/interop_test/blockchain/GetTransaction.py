from boa3.builtin import public
from boa3.builtin.interop.blockchain import get_transaction, Transaction
from boa3.builtin.type import UInt256


@public
def main(hash_: UInt256) -> Transaction:
    return get_transaction(hash_)
