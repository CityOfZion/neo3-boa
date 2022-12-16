from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.gas import GAS as GAS_CONTRACT
from boa3.builtin.type import UInt160


@public
def main(account: UInt160) -> int:
    return GAS_CONTRACT.balanceOf(account)
