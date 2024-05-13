from boa3.sc.contracts import NeoToken
from boa3.sc.types import UInt160


def main(account: UInt160) -> int:
    return NeoToken.balanceOf(account, 'arg')
