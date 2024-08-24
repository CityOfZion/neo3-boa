from boa3.sc.compiletime import public
from boa3.sc.contracts import NeoToken
from boa3.sc.types import UInt160


@public
def main(account: UInt160) -> int:
    return NeoToken.balanceOf(account)
