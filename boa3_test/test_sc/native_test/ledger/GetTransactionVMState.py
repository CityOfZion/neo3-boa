from boa3.sc.compiletime import public
from boa3.sc.contracts import LedgerContract
from boa3.sc.types import UInt256, VMState


@public
def main(hash_: UInt256) -> VMState:
    return LedgerContract.get_transaction_vm_state(hash_)
