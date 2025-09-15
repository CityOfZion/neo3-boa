from boa3.internal.model.builtin.interop.contract import ContractType
from boa3.internal.model.builtin.interop.nativecontract import ContractManagementMethod
from boa3.internal.model.variable import Variable


class GetContractByIdMethod(ContractManagementMethod):

    def __init__(self, contract_type: ContractType):
        from boa3.internal.model.type.type import Type

        identifier = 'get_contract_by_id'
        syscall = 'getContractById'
        args: dict[str, Variable] = {
            'contract_id': Variable(Type.int),
        }

        super().__init__(identifier, syscall, args, return_type=contract_type)
