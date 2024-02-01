from typing import Any

from boa3.builtin.compile_time import NeoMetadata, public
from boa3.builtin.type import UInt160
from boa3_test.test_sc.metadata_test.aux_package import internal_package


@public
def Main() -> int:
    return 5


def standards_manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.supported_standards = ['NEP-17']
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
    internal_package.method_called(from_address, to_address, amount)
    return True
