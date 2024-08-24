from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.contracts import NeoToken
from boa3.sc.types import UInt160


@public
def main(from_address: UInt160, to_address: UInt160, amount: int, data: Any) -> int:
    return NeoToken.transfer(from_address, to_address, amount, data)
