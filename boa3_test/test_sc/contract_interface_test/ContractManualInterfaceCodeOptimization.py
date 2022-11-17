from typing import Any, cast

from boa3.builtin import public
from boa3.builtin.interop.contract import call_contract
from boa3.builtin.type import UInt160


class Nep17:
    _hash = UInt160(b'\x6c\x24\xb4\xda\x62\x25\xe9\x29\x29\x99\x52\xa9\x21\xea\x59\x24\xc3\xdd\xdc\x53')

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
