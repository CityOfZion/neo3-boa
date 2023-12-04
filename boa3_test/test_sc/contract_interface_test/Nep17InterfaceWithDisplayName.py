from typing import Any

from boa3.builtin.compile_time import contract, public
from boa3.builtin.type import UInt160


@contract('0x3d72a4a577ed06af3ba968e7c73cd8df65c49d52')
class Nep17:

    @staticmethod
    def symbol() -> str:
        pass

    @staticmethod
    def decimals() -> int:
        pass

    @staticmethod
    def totalSupply() -> int:
        pass

    @staticmethod
    def balanceOf(account: UInt160) -> int:
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
    return Nep17.totalSupply()


@public
def nep17_balance_of(account: UInt160) -> int:
    return Nep17.balanceOf(account)


@public
def nep17_transfer(from_account: UInt160, to_account: UInt160, amount: int, additional_data: Any) -> bool:
    return Nep17.transfer(from_account, to_account, amount, additional_data)
