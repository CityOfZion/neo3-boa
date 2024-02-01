from boa3.builtin.compile_time import public
from boa3.builtin.contract import Nep17Contract
from boa3.builtin.interop.blockchain import get_contract
from boa3.builtin.interop.contract import NEO
from boa3.builtin.type import UInt160


@public
def main(from_address: UInt160, to_address: UInt160, amount: int) -> bool:
    nep_17_contract: Nep17Contract = get_contract(NEO)
    contract_transfer = nep_17_contract.transfer(from_address, to_address, amount)
    return contract_transfer
