from typing import Dict

from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.variable import Variable


class CheckSigMethod(InteropMethod):

    _RAW_BYTES = b''

    def __init__(self):
        from boa3.model.type.type import Type
        from boa3.model.type.collection.sequence.ecpointtype import ECPointType

        identifier = 'check_sig'
        syscall = 'System.Crypto.CheckSig'
        args: Dict[str, Variable] = {
            'pubkeys': Variable(ECPointType.build()),
            'signatures': Variable(Type.bytes)
        }
        super().__init__(identifier, syscall, args, return_type=Type.bool)

    @classmethod
    def get_raw_bytes(cls) -> bytes:
        if len(cls._RAW_BYTES) == 0:
            from boa3.compiler.codegenerator import get_bytes
            check_sig = CheckSigMethod()
            cls._RAW_BYTES = get_bytes(check_sig.opcode)

        return cls._RAW_BYTES
