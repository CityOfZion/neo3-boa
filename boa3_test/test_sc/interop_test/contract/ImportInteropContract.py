from typing import Any

from boa3.builtin import interop, type
from boa3.sc.compiletime import NeoMetadata, public
from boa3.sc.utils import call_contract


@public
def call_flags_all() -> interop.contract.CallFlags:
    return interop.contract.CallFlags.ALL


@public
def main(scripthash: type.UInt160, method: str, args: list) -> Any:
    return call_contract(scripthash, method, args)


def manifest_metadata() -> NeoMetadata:
    # since this smart contract will call another, it needs to have permission to do so on the manifest
    meta = NeoMetadata()
    meta.add_permission(contract='*', methods='*')
    return meta
