from typing import Dict

from boa3.model.builtin.interop.contract.contracttype import ContractType
from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.variable import Variable


class GetContractMethod(InteropMethod):

    def __init__(self, contract_type: ContractType):
        from boa3.model.type.type import Type
        identifier = 'get_contract'
        syscall = 'System.Blockchain.GetContract'
        args: Dict[str, Variable] = {'hash': Variable(Type.bytes)}
        super().__init__(identifier, syscall, args, return_type=contract_type)
