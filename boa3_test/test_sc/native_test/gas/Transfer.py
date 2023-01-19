from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.gas import GAS
from boa3.builtin.type import UInt160


@public
def main(from_address: UInt160, to_address: UInt160, amount: int, data: Any) -> bool:
    return GAS.transfer(from_address, to_address, amount, data)
