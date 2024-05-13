from boa3.sc.compiletime import public
from boa3.sc.contracts import ContractManagement
from boa3.sc.types import UInt160


@public
def main(hash: UInt160, method: str, parameter_count: int) -> bool:
    return ContractManagement.has_method(hash, method, parameter_count)
