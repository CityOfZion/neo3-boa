from typing import Dict

from boa3.internal.model.builtin.interop.contract.contracttype import ContractType
from boa3.internal.model.builtin.interop.nativecontract.ContractManagement.contractmanagementmethod import \
    ContractManagementMethod
from boa3.internal.model.variable import Variable


class GetContractMethod(ContractManagementMethod):

    def __init__(self, contract_type: ContractType):
        from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type
        from boa3.internal.model.type.type import Type
        identifier = 'get_contract'
        syscall = 'getContract'
        args: Dict[str, Variable] = {'hash': Variable(UInt160Type.build())}
        super().__init__(identifier, syscall, args, return_type=Type.optional.build(contract_type))
