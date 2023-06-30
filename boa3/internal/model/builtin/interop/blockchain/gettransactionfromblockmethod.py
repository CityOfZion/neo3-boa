from typing import Dict

from boa3.internal.model.builtin.interop.blockchain.transactiontype import TransactionType
from boa3.internal.model.builtin.interop.nativecontract import LedgerMethod
from boa3.internal.model.variable import Variable


class GetTransactionFromBlockMethod(LedgerMethod):

    def __init__(self, transaction_type: TransactionType):
        from boa3.internal.model.type.collection.sequence.uint256type import UInt256Type
        from boa3.internal.model.type.type import Type

        identifier = 'get_transaction_from_block'
        syscall = 'getTransactionFromBlock'
        args: Dict[str, Variable] = {'block_hash_or_height': Variable(Type.union.build([UInt256Type.build(),
                                                                                        Type.int])),
                                     'tx_index': Variable(Type.int)}
        super().__init__(identifier, syscall, args, return_type=Type.optional.build(transaction_type))
