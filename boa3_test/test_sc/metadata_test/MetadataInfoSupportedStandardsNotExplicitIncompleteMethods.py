from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.types import UInt160
from boa3.sc.utils import Nep17TransferEvent

on_transfer = Nep17TransferEvent


@public
def main() -> int:
    return 5


@public(safe=True)
def symbol() -> str:
    pass


@public(safe=True)
def decimals() -> int:
    pass


@public(name='balanceOf', safe=True)
def balance_of(account: UInt160) -> int:
    pass


@public
def transfer(from_address: UInt160, to_address: UInt160, amount: int, data: Any) -> bool:
    pass
