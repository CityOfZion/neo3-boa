from typing import Any

import boa3_test.examples.nep17 as nep17
from boa3.builtin.compile_time import NeoMetadata, public
from boa3.builtin.type import UInt160


def standards_manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.supported_standards = ['NEP-17']
    return meta


@public(safe=True)
def symbol() -> str:
    return nep17.symbol()


@public(safe=True)
def decimals() -> int:
    return nep17.decimals()


@public(name='totalSupply', safe=True)
def total_supply() -> int:
    return nep17.total_supply()


@public(name='balanceOf', safe=True)
def balance_of(account: UInt160) -> int:
    return nep17.balance_of(account)


@public
def transfer(from_address: UInt160, to_address: UInt160, amount: int, data: Any) -> bool:
    return nep17.transfer(from_address, to_address, amount, data)
