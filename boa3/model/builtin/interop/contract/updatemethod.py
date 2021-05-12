from typing import Dict

from boa3.model.builtin.interop.nativecontract import ContractManagementMethod
from boa3.model.variable import Variable


class UpdateMethod(ContractManagementMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'update_contract'
        syscall = 'update'
        args: Dict[str, Variable] = {
            'nef_file': Variable(Type.bytes),
            'manifest': Variable(Type.bytes)
        }
        super().__init__(identifier, syscall, args, return_type=Type.none)
