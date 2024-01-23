from boa3.internal.model.builtin.interop.blockchain.blocktype import BlockType
from boa3.internal.model.builtin.interop.nativecontract import LedgerMethod
from boa3.internal.model.variable import Variable


class GetBlockMethod(LedgerMethod):

    def __init__(self, block_type: BlockType):
        from boa3.internal.model.type.collection.sequence.uint256type import UInt256Type
        from boa3.internal.model.type.type import Type

        identifier = 'get_block'
        syscall = 'getBlock'
        args: dict[str, Variable] = {'index': Variable(Type.union.build([Type.int,
                                                                         UInt256Type.build()]))}
        super().__init__(identifier, syscall, args, return_type=Type.optional.build(block_type))
