from typing import Any

from boa3.sc.compiletime import NeoMetadata, public
from boa3.sc.types import UInt160
from boa3.sc.utils import CreateNewEvent
from boa3.sc.utils.iterator import Iterator

on_transfer = CreateNewEvent(
    # trigger when tokens are transferred, including zero value transfers.
    [
        ('from_addr', UInt160 | None),
        ('to_addr', UInt160 | None),
        ('amount', int),
        ('tokenId', str)
    ],
    'Transfer'
)


def standards_manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.supported_standards = ['NEP-11']
    return meta


@public(safe=True)
def symbol() -> str:
    pass


@public(safe=True)
def decimals() -> int:
    pass


@public(safe=True)
def totalSupply() -> int:
    pass


@public(safe=True)
def balanceOf(owner: UInt160) -> int:
    pass


@public(safe=True)
def tokensOf(owner: UInt160) -> Iterator:
    pass


@public
def transfer(to: UInt160, tokenId: str, data: Any) -> bool:
    on_transfer(to, to, 1, tokenId)
    pass


@public(safe=True)
def ownerOf(tokenId: str) -> UInt160:
    pass


@public(safe=True)
def tokens() -> Iterator:
    pass


@public(safe=True)
def properties(tokenId: str) -> dict[Any, Any]:
    pass
