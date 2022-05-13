from typing import List, Tuple

from boa3.model.builtin.method import ScriptHashMethod
from boa3.model.type.collection.sequence.ecpointtype import ECPointType
from boa3.model.type.type import IType
from boa3.neo.vm.opcode.Opcode import Opcode


class ECPointToScriptHashMethod(ScriptHashMethod):

    def __init__(self, data_type: IType = None):
        ec_point = ECPointType.build()
        if not ec_point.is_type_of(data_type):
            data_type = ec_point

        super().__init__(data_type)

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3 import constants
        from boa3.model.builtin.interop.crypto.checksigmethod import CheckSigMethod
        from boa3.model.builtin.interop.crypto.sha256method import Sha256Method
        from boa3.model.builtin.interop.crypto.ripemd160method import Ripemd160Method
        from boa3.model.type.type import Type

        # build CheckSig script
        pushdata, pushbytes = Opcode.get_pushdata_and_data_from_size(constants.SIZE_OF_ECPOINT)
        opcodes = [
            Opcode.get_pushdata_and_data(pushdata + pushbytes),
            (Opcode.SWAP, b''),
            Opcode.get_pushdata_and_data(CheckSigMethod.get_raw_bytes()),
            (Opcode.CAT, b''),
            (Opcode.CAT, b''),
        ]

        opcodes.extend([Opcode.get_push_and_data(1),  # pack argument to call syscall
                        (Opcode.PACK, b'')
                        ] + Sha256Method().opcode
                       )
        opcodes.extend([Opcode.get_push_and_data(1),  # pack argument to call syscall
                        (Opcode.PACK, b'')
                        ] + Ripemd160Method().opcode
                       )

        opcodes.extend([
            # limit result to UInt160 length
            Opcode.get_push_and_data(0),
            Opcode.get_push_and_data(constants.SIZE_OF_INT160),
            (Opcode.SUBSTR, b''),
            (Opcode.CONVERT, Type.bytes.stack_item)
        ])
        return opcodes
