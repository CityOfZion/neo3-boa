from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.contractmanagement import ContractManagement
from boa3.builtin.type import UInt160


@public
def main(hash: UInt160, method: str, parameter_count: int) -> bool:
    return ContractManagement.has_method(hash, method, parameter_count)
