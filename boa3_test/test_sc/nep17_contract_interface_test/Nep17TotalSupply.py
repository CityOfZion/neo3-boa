from boa3.sc.compiletime import public
from boa3.sc.contracts import ContractManagement, NeoToken
from boa3.sc.types import Nep17Contract


@public
def main() -> int:
    nep_17_contract: Nep17Contract = ContractManagement.get_contract(NeoToken.hash)
    contract_total_supply = nep_17_contract.total_supply()
    return contract_total_supply
