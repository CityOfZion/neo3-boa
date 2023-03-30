from typing import Dict

from boa3.internal.model.builtin.interop.blockchain.signertype import SignerType
from boa3.internal.model.builtin.interop.nativecontract import LedgerMethod
from boa3.internal.model.variable import Variable


class GetTransactionSignersMethod(LedgerMethod):

    def __init__(self, signer_type: SignerType):
        from boa3.internal.model.type.collection.sequence.uint256type import UInt256Type
        from boa3.internal.model.type.type import Type

        identifier = 'get_transaction_signers'
        syscall = 'getTransactionSigners'
        args: Dict[str, Variable] = {'hash_': Variable(UInt256Type.build())}
        super().__init__(identifier, syscall, args, return_type=Type.list.build([signer_type]))
