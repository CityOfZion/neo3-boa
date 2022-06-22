from typing import Dict, List, Tuple

from boa3.model.builtin.interop.nativecontract import NeoContractMethod
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class UnVoteMethod(NeoContractMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        from boa3.model.type.collection.sequence.uint160type import UInt160Type

        identifier = 'un_vote'
        native_identifier = ''  # un_vote is not neo native
        args: Dict[str, Variable] = {
            'account': Variable(UInt160Type.build()),
        }

        super().__init__(identifier, native_identifier, args, return_type=Type.bool)

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.model.builtin.native.nativecontract import NativeContract
        return (
            [
                (Opcode.UNPACK, b''),
                (Opcode.DROP, b''),
                (Opcode.PUSHNULL, b''),
                (Opcode.SWAP, b''),
                (Opcode.PUSH2, b''),
                (Opcode.PACK, b''),
            ] +
            NativeContract.NEO.class_methods['vote'].opcode
        )
