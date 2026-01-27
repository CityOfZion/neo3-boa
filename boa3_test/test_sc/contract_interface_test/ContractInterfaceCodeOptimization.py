from typing import Any

from boa3.sc.compiletime import contract, display_name, public
from boa3.sc.types import UInt160


@contract('0x3d1f9a6609c192b4de23e54b0a9430268a1d34ea')
class Nep17:

    @staticmethod
    def symbol() -> str:
        pass

    @staticmethod
    def decimals() -> int:
        pass

    @staticmethod
    @display_name('totalSupply')
    def total_supply() -> int:
        pass

    @staticmethod
    @display_name('balanceOf')
    def balance_of(account: UInt160) -> int:
        pass

    @staticmethod
    def transfer(from_address: UInt160, to_address: UInt160, amount: int, data: Any) -> bool:
        pass


@public
def nep17_symbol() -> str:
    return Nep17.symbol()
