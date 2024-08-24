from boa3.sc.compiletime import public
from boa3.sc.contracts import ContractManagement, NeoToken
from boa3.sc.types import Nep17Contract


@public
def main() -> str:
    nep_17_contract: Nep17Contract = ContractManagement.get_contract(NeoToken.hash)
    contract_symbol = nep_17_contract.symbol()
    return contract_symbol
