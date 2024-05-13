from boa3.sc.compiletime import public
from boa3.sc.contracts import ContractManagement
from boa3.sc.types import UInt160, Contract


@public
def main(hash: UInt160) -> Contract | None:
    return ContractManagement.get_contract(hash)
