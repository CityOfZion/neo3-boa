from typing import Any, cast

from boa3.builtin.compile_time import public
from boa3.builtin.interop.contract import call_contract
from boa3.builtin.type import UInt160


class Nep17:
    _hash = UInt160(b'\x13\x28\xe7\x60\x1d\x73\xe3\x9f\x54\x3e\xc3\xec\xf3\xf1\xb7\x49\xa7\x26\x3e\xc0')

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
