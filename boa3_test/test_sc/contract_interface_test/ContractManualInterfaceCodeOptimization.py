from typing import Any, cast

from boa3.sc.compiletime import public
from boa3.sc.types import UInt160
from boa3.sc.utils import call_contract


class Nep17:
    _hash = UInt160(b'\x43\x90\xae\x37\x4e\xa2\x53\x8b\x8b\xb2\x01\xfb\xf9\xdb\x88\x30\xb1\x3b\x7f\x32')

    @classmethod
    def symbol(cls) -> str:
        return cast(str, call_contract(cls._hash, 'symbol'))

    @classmethod
    def decimals(cls) -> int:
        return cast(int, call_contract(cls._hash, 'decimals'))

    @classmethod
    def total_supply(cls) -> int:
        return cast(int, call_contract(cls._hash, 'totalSupply'))

    @classmethod
    def balance_of(cls, account: UInt160) -> int:
        return cast(int, call_contract(cls._hash, 'balanceOf', [account]))

    @classmethod
    def transfer(cls, from_address: UInt160, to_address: UInt160, amount: int, data: Any) -> bool:
        return cast(bool, call_contract(cls._hash, 'transfer', [from_address, to_address, amount, data]))


@public
def nep17_symbol() -> str:
    return Nep17.symbol()
