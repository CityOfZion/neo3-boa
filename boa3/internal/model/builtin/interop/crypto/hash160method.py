from typing import Dict

from boa3.internal.model.builtin.interop.nativecontract import CryptoLibMethod
from boa3.internal.model.variable import Variable


class Hash160Method(CryptoLibMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = 'hash160'
        native_identifier = ''  # hash160 is not neo native
        args: Dict[str, Variable] = {'key': Variable(Type.any)}
        super().__init__(identifier, native_identifier, args, return_type=Type.bytes)

    @property
    def pack_arguments(self) -> bool:
        if self._pack_arguments is None:
            from boa3.internal.model.builtin.interop.interop import Interop
            self._pack_arguments = Interop.Sha256.pack_arguments  # this is the first method called
        return self._pack_arguments

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.interop.interop import Interop

        code_generator.convert_builtin_method_call(Interop.Sha256, is_internal=True)
        code_generator.convert_builtin_method_call(Interop.Ripemd160, is_internal=True)
