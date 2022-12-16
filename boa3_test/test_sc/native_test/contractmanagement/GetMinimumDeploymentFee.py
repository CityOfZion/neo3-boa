from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.contractmanagement import ContractManagement


@public
def main() -> int:
    return ContractManagement.get_minimum_deployment_fee()
