from typing import Any

from boa3.sc.compiletime import NeoMetadata, public
from boa3.sc.types import UInt160
from boa3.sc.utils import Nep17TransferEvent

on_transfer = Nep17TransferEvent


@public
def Main() -> int:
    return 5


def standards_manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.supported_standards = [
        'NEP-17', 'NEP-17.1', 'NEP-17.1.2', 'NEP-17.1.3.5.7.9.11.13',
        'nep 100', 'nEP101', 'Nep-102', 'not neo standard 1'
    ]
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
def balance_of(account: UInt160) -> int:
    pass


@public
def transfer(from_address: UInt160, to_address: UInt160, amount: int, data: Any) -> bool:
    pass
