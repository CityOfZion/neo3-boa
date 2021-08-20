from typing import Any

from boa3.builtin import public
from boa3.builtin.nativecontract.contractmanagement import ContractManagement


@public
def main(arg: Any) -> int:
    return ContractManagement.get_minimum_deployment_fee(arg)
