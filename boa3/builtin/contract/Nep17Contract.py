from typing import Any

from boa3.builtin.interop.contract import Contract
from boa3.builtin.type import UInt160


class Nep17Contract(Contract):
    def symbol(self) -> str:
        pass

    def decimals(self) -> int:
        pass

    def total_supply(self) -> int:
        pass

    def balance_of(self, account: UInt160) -> int:
        pass

    def transfer(self, from_address: UInt160, to_address: UInt160, amount: int, data: Any = None) -> bool:
        pass
