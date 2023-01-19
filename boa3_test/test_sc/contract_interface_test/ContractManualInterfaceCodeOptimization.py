from typing import Any, cast

from boa3.builtin.compile_time import public
from boa3.builtin.interop.contract import call_contract
from boa3.builtin.type import UInt160


class Nep17:
    _hash = UInt160(b'\x42\x60\x25\x8d\x83\xf8\xb6\x4e\x44\xeb\xe6\x21\x92\x72\xa8\x38\x75\x0e\x37\xcc')

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
