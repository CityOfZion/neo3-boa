from boa3.internal.model.builtin.interop.nativecontract import ContractManagementMethod
from boa3.internal.model.variable import Variable


class DestroyMethod(ContractManagementMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = 'destroy_contract'
        syscall = 'destroy'
        args: dict[str, Variable] = {}
        super().__init__(identifier, syscall, args, return_type=Type.none)
