from boa3.internal.model.builtin.interop.nativecontract import ContractManagementMethod
from boa3.internal.model.type.type import Type
from boa3.internal.model.variable import Variable


class GetMinimumDeploymentFeeMethod(ContractManagementMethod):

    def __init__(self):
        identifier = 'get_minimum_deployment_fee'
        syscall = 'getMinimumDeploymentFee'
        args: dict[str, Variable] = {}
        super().__init__(identifier, syscall, args, return_type=Type.int)
