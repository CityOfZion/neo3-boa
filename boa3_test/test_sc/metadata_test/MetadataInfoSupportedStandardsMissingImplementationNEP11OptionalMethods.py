from typing import Any

from boa3.sc.compiletime import NeoMetadata, public
from boa3.sc.types import UInt160
from boa3.sc.utils import Nep11TransferEvent
from boa3.sc.utils.iterator import Iterator

on_transfer = Nep11TransferEvent


def standards_manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.supported_standards = ['NEP-11']  # for nep11, boa checks if the standard is implemented
    return meta


# this method has the same name as an NEP-11 optional method, but with a different signature
@public(safe=True)
def properties(token_id: int) -> dict[Any, Any]:
    pass


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


@public(name='ownerOf', safe=True)
def owner_of(token_id: bytes) -> UInt160:
    pass


@public
def transfer(to_address: UInt160, token_id: bytes, data: Any) -> bool:
    pass
