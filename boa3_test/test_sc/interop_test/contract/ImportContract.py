from typing import Any

from boa3.builtin.compile_time import NeoMetadata, public
from boa3.builtin.interop import contract
from boa3.builtin.type import UInt160


@public
def call_flags_all() -> contract.CallFlags:
    return contract.CallFlags.ALL


@public
def main(scripthash: UInt160, method: str, args: list) -> Any:
    return contract.call_contract(scripthash, method, args)


def manifest_metadata() -> NeoMetadata:
    # since this smart contract will call another, it needs to have permission to do so on the manifest
    meta = NeoMetadata()
    meta.add_permission(contract='*', methods='*')
    return meta
