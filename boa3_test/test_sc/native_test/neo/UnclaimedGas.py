from boa3.sc.compiletime import public
from boa3.sc.contracts import NeoToken
from boa3.sc.types import UInt160


@public
def main(account: UInt160, index: int) -> int:
    return NeoToken.unclaimed_gas(account, index)
