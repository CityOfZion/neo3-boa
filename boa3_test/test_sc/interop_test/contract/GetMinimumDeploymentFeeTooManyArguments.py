from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.contracts import ContractManagement


@public
def main(arg: Any) -> int:
    return ContractManagement.get_minimum_deployment_fee(arg)
