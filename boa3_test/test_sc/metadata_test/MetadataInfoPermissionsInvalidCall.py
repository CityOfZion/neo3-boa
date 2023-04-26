from typing import Any

from boa3.builtin.compile_time import NeoMetadata, metadata, public
from boa3.builtin.interop.contract import call_contract, NEO
from boa3.builtin.type import UInt160


@metadata
def permissions_manifest() -> NeoMetadata:
    meta = NeoMetadata()

    meta.add_permission(contract='0x0102030405060708090A0B0C0D0E0F1011121314', methods='*')

    return meta


@public
def main() -> Any:
    return call_contract(UInt160(NEO), 'transfer', [UInt160(NEO), UInt160(NEO), 1, None])
