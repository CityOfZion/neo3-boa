from boa3.internal.model.builtin.interop.nativecontract import LedgerMethod
from boa3.internal.model.variable import Variable


class GetTransactionHeightMethod(LedgerMethod):

    def __init__(self):
        from boa3.internal.model.type.collection.sequence.uint256type import UInt256Type
        from boa3.internal.model.type.type import Type

        identifier = 'get_transaction_height'
        syscall = 'getTransactionHeight'
        args: dict[str, Variable] = {'hash_': Variable(UInt256Type.build())}
        super().__init__(identifier, syscall, args, return_type=Type.int)
