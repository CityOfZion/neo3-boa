from boa3.sc.compiletime import public
from boa3.sc.contracts import ContractManagement, NeoToken
from boa3.sc.types import UInt160, Nep17Contract


@public
def main(from_address: UInt160, to_address: UInt160, amount: int) -> bool:
    nep_17_contract: Nep17Contract = ContractManagement.get_contract(NeoToken.hash)
    contract_transfer = nep_17_contract.transfer(from_address, to_address, amount)
    return contract_transfer
