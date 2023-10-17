from boa3.builtin.compile_time import public
from boa3.builtin.contract import Nep17Contract
from boa3.builtin.interop.blockchain import get_contract
from boa3.builtin.interop.contract import NEO


@public
def main() -> int:
    nep_17_contract: Nep17Contract = get_contract(NEO)
    contract_decimals = nep_17_contract.decimals()
    return contract_decimals
