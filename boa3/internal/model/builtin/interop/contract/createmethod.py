import ast

from boa3.internal.model.builtin.interop.contract.contracttype import ContractType
from boa3.internal.model.builtin.interop.nativecontract import ContractManagementMethod
from boa3.internal.model.variable import Variable


class CreateMethod(ContractManagementMethod):

    def __init__(self, contract_type: ContractType):
        from boa3.internal.model.type.type import Type
        identifier = 'create_contract'
        syscall = 'deploy'
        args: dict[str, Variable] = {
            'nef_file': Variable(Type.bytes),
            'manifest': Variable(Type.bytes),
            'data': Variable(Type.any)
        }
        data_default = ast.parse("{0}".format(Type.any.default_value)
                                 ).body[0].value

        super().__init__(identifier, syscall, args, defaults=[data_default], return_type=contract_type)
