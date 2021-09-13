from boa3.builtin import public
from boa3.builtin.interop.contract import Contract
from boa3.builtin.nativecontract.contractmanagement import ContractManagement
from boa3.builtin.type import UInt160


@public
def main(hash: UInt160) -> Contract:
    return ContractManagement.get_contract(hash)
