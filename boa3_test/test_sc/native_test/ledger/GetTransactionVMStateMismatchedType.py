from boa3.builtin.interop.blockchain import VMState
from boa3.builtin.nativecontract.ledger import Ledger


def main() -> VMState:
    return Ledger.get_transaction_vm_state(123)
