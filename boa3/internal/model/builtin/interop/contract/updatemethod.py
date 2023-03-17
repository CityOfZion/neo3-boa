import ast
from typing import Dict

from boa3.internal.model.builtin.interop.nativecontract import ContractManagementMethod
from boa3.internal.model.variable import Variable


class UpdateMethod(ContractManagementMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = 'update_contract'
        syscall = 'update'
        args: Dict[str, Variable] = {
            'nef_file': Variable(Type.bytes),
            'manifest': Variable(Type.bytes),
            'data': Variable(Type.any)
        }
        data_default = ast.parse("{0}".format(Type.any.default_value)
                                 ).body[0].value
        super().__init__(identifier, syscall, args, defaults=[data_default], return_type=Type.none)
