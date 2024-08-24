from boa3.sc.compiletime import public
from boa3.sc.contracts import GasToken as GAS_CONTRACT
from boa3.sc.types import UInt160


@public
def main(account: UInt160) -> int:
    return GAS_CONTRACT.balanceOf(account)
