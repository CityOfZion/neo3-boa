from boa3.sc import contracts
from boa3.sc.compiletime import public
from boa3.sc.types import UInt160, Contract


@public
def main(hash_: UInt160) -> Contract | None:
    return contracts.ContractManagement.get_contract(hash_)
