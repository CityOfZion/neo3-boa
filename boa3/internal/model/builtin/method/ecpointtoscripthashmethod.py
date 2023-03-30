from typing import List, Tuple

from boa3.internal.model.builtin.method import ScriptHashMethod
from boa3.internal.model.type.collection.sequence.ecpointtype import ECPointType
from boa3.internal.model.type.type import IType
from boa3.internal.neo.vm.opcode import OpcodeHelper
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class ECPointToScriptHashMethod(ScriptHashMethod):

    def __init__(self, data_type: IType = None):
        ec_point = ECPointType.build()
        if not ec_point.is_type_of(data_type):
            data_type = ec_point

        super().__init__(data_type)

    @property
    def _opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.internal import constants
        from boa3.internal.model.builtin.interop.crypto.checksigmethod import CheckSigMethod
        from boa3.internal.model.builtin.interop.crypto.sha256method import Sha256Method
        from boa3.internal.model.builtin.interop.crypto.ripemd160method import Ripemd160Method
        from boa3.internal.model.type.type import Type

        # build CheckSig script
        pushdata, pushbytes = OpcodeHelper.get_pushdata_and_data_from_size(constants.SIZE_OF_ECPOINT)
        opcodes = [
            OpcodeHelper.get_pushdata_and_data(pushdata + pushbytes),
            (Opcode.SWAP, b''),
            OpcodeHelper.get_pushdata_and_data(CheckSigMethod.get_raw_bytes()),
            (Opcode.CAT, b''),
            (Opcode.CAT, b''),
        ]

        opcodes.extend(Sha256Method().opcode)
        opcodes.extend(Ripemd160Method().opcode)

        opcodes.extend([
            # limit result to UInt160 length
            OpcodeHelper.get_push_and_data(0),
            OpcodeHelper.get_push_and_data(constants.SIZE_OF_INT160),
            (Opcode.SUBSTR, b''),
            (Opcode.CONVERT, Type.bytes.stack_item)
        ])
        return opcodes
