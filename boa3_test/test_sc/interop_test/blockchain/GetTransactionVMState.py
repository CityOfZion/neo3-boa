from boa3.builtin.compile_time import public
from boa3.builtin.interop.blockchain import VMState, get_transaction_vm_state
from boa3.builtin.type import UInt256


@public
def main(hash_: UInt256) -> VMState:
    return get_transaction_vm_state(hash_)
