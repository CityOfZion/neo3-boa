from typing import Any, cast

from boa3.sc.compiletime import public
from boa3.sc.types import UInt160
from boa3.sc.utils import call_contract


class Nep17:
    _hash = UInt160(b'\xea\x34\x1d\x8a\x26\x30\x94\x0a\x4b\xe5\x23\xde\xb4\x92\xc1\x09\x66\x9a\x1f\x3d')

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
