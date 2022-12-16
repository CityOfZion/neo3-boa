from boa3.builtin.compile_time import public
from boa3.builtin.interop.blockchain import get_transaction_height
from boa3.builtin.type import UInt256


@public
def main(hash_: UInt256) -> int:
    return get_transaction_height(hash_)
