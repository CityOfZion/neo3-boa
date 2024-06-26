from boa3.builtin.compile_time import public
from boa3.builtin.interop.blockchain import Transaction, get_transaction
from boa3.builtin.type import UInt256


@public
def main(hash_: UInt256) -> Transaction | None:
    return get_transaction(hash_)
