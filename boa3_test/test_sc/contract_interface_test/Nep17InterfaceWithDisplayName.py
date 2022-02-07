from typing import Any

from boa3.builtin import contract, display_name, public
from boa3.builtin.type import UInt160


@contract('0x5695642fcf208fc8b55c6163b3518afd7d35ff02')
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
    @display_name('totalSupply')
    def total_supply_2(a: int) -> int:
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


@public
def nep17_decimals() -> int:
    return Nep17.decimals()


@public
def nep17_total_supply() -> int:
    return Nep17.total_supply()


@public
def nep17_balance_of(account: UInt160) -> int:
    return Nep17.balance_of(account)


@public
def nep17_transfer(from_account: UInt160, to_account: UInt160, amount: int, additional_data: Any) -> bool:
    return Nep17.transfer(from_account, to_account, amount, additional_data)
