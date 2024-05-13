from boa3.sc.compiletime import public
from boa3.sc.contracts import ContractManagement, NeoToken
from boa3.sc.types import UInt160, Nep17Contract


@public
def main(account: UInt160) -> int:
    nep_17_contract: Nep17Contract = ContractManagement.get_contract(NeoToken.hash)
    contract_balance_of = nep_17_contract.balance_of(account)
    return contract_balance_of
