from typing import Dict, List, Tuple

from boa3.internal.model.builtin.interop.nativecontract import CryptoLibMethod
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class Hash256Method(CryptoLibMethod):
    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = 'hash256'
        native_identifier = ''  # hash256 is not neo native
        args: Dict[str, Variable] = {'key': Variable(Type.any)}
        super().__init__(identifier, native_identifier, args, return_type=Type.bytes)

    @property
    def pack_arguments(self) -> bool:
        if self._pack_arguments is None:
            from boa3.internal.model.builtin.interop.interop import Interop
            self._pack_arguments = Interop.Sha256.pack_arguments  # this is the first method called
        return self._pack_arguments

    @property
    def _opcode(self) -> List[Tuple[Opcode, bytes]]:
        # calls the generic implementation to ensure the correct output when calling consecutive compilations
        default_opcodes = super()._opcode
        from boa3.internal.model.builtin.interop.interop import Interop
        return (Interop.Sha256.opcode
                + Interop.Sha256.opcode)
