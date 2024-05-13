from boa3.sc.compiletime import public
from boa3.sc.contracts import ContractManagement


@public
def main() -> int:
    return ContractManagement.get_minimum_deployment_fee()
