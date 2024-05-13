from typing import Any

from boa3.sc.contracts import GasToken
from boa3.sc.types import UInt160


def main(from_address: UInt160, to_address: UInt160, amount: int, data: Any) -> bool:
    return GasToken.transfer(from_address, to_address, amount, data, 'arg')
