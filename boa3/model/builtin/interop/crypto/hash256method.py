from typing import Dict, List, Tuple

from boa3.model.builtin.interop.crypto.cryptolibmethod import CryptoLibMethod
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class Hash256Method(CryptoLibMethod):
    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'hash256'
        syscall = ''
        args: Dict[str, Variable] = {'key': Variable(Type.any)}
        super().__init__(identifier, syscall, args, return_type=Type.bytes)

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.model.builtin.interop.interop import Interop
        return (Interop.Sha256.opcode
                + [(Opcode.PUSH1, b''),
                   (Opcode.PACK, b'')
                   ]
                + Interop.Sha256.opcode)
