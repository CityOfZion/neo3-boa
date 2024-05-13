from boa3.sc.compiletime import public
from boa3.sc.contracts import NeoToken
from boa3.sc.types import UInt160


@public
def main(from_address: UInt160, to_address: UInt160, amount: int) -> int:
    return NeoToken.transfer(from_address, to_address, amount)
