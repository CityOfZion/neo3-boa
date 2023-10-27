from boa3.builtin.compile_time import public
from boa3.builtin.contract import Nep17Contract
from boa3.builtin.interop.blockchain import get_contract
from boa3.builtin.interop.contract import NEO
from boa3.builtin.type import UInt160


@public
def main(account: UInt160) -> int:
    nep_17_contract: Nep17Contract = get_contract(NEO)
    contract_balance_of = nep_17_contract.balance_of(account)
    return contract_balance_of
