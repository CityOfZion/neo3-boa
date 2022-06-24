from boa3.builtin.interop.blockchain import VMState, get_transaction_vm_state


def main() -> VMState:
    return get_transaction_vm_state(123)
