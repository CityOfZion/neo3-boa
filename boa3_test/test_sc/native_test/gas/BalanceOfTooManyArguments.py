from boa3.sc.contracts import GasToken
from boa3.sc.types import UInt160


def main(account: UInt160) -> int:
    return GasToken.balanceOf(account, 'arg')
