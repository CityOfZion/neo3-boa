from boa3.sc.contracts import LedgerContract
from boa3.sc.types import VMState


def main() -> VMState:
    return LedgerContract.get_transaction_vm_state(123)
