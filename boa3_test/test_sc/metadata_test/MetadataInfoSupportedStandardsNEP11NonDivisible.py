from typing import Any

from boa3.builtin.compile_time import NeoMetadata, public
from boa3.builtin.contract import Nep11TransferEvent
from boa3.builtin.interop.iterator import Iterator
from boa3.builtin.type import UInt160

on_transfer = Nep11TransferEvent


def standards_manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.supported_standards = ['NEP-11']  # for nep11, boa checks if the standard is implemented
    return meta


@public(safe=True)
def symbol() -> str:
    pass


@public(safe=True)
def decimals() -> int:
    pass


@public(name='totalSupply', safe=True)
def total_supply() -> int:
    pass


@public(name='balanceOf', safe=True)
def balance_of(owner_address: UInt160) -> int:
    pass


@public(name='tokensOf', safe=True)
def tokens_of(owner: UInt160) -> Iterator:
    pass


@public
def transfer(to_address: UInt160, token_id: bytes, data: Any) -> bool:
    pass


@public(name='ownerOf', safe=True)
def owner_of_non_divisible(token_id: bytes) -> UInt160:
    pass
