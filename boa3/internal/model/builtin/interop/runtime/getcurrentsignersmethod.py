from boa3.internal.model.builtin.interop.blockchain import SignerType
from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.variable import Variable

class GetCurrentSignersMethod(InteropMethod):
    def __init__(self, signer_type: SignerType):
        from boa3.internal.model.type.type import Type
        identifier = 'get_current_signers'
        syscall = 'System.Runtime.CurrentSigners'
        args: dict[str, Variable] = {}
        super().__init__(identifier, syscall, args, return_type=Type.list.build([signer_type]))
