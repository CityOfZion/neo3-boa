from typing import Dict, List, Tuple

from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class Hash160Method(InteropMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'hash160'
        syscall = ''
        args: Dict[str, Variable] = {'key': Variable(Type.any)}
        super().__init__(identifier, syscall, args, return_type=Type.bytes)

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.model.builtin.interop.interop import Interop
        return Interop.Sha256.opcode + Interop.Ripemd160.opcode
