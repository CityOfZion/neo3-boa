from typing import Dict

from boa3.model.builtin.interop.blockchain.vmstatetype import VMStateType
from boa3.model.builtin.interop.nativecontract import LedgerMethod
from boa3.model.variable import Variable


class GetTransactionVMStateMethod(LedgerMethod):

    def __init__(self, vm_state_type: VMStateType):
        from boa3.model.type.collection.sequence.uint256type import UInt256Type

        identifier = 'get_transaction_vm_state'
        syscall = 'getTransactionVMState'
        args: Dict[str, Variable] = {'hash_': Variable(UInt256Type.build())}
        super().__init__(identifier, syscall, args, return_type=vm_state_type)
