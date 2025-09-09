from typing import Any

from boa3.sc import utils
from boa3.sc.compiletime import NeoMetadata, public
from boa3.sc.types import UInt160, CallFlags


@public
def call_flags_all() -> CallFlags:
    return CallFlags.ALL


@public
def main(scripthash: UInt160, method: str, args: list) -> Any:
    return utils.call_contract(scripthash, method, args)


def manifest_metadata() -> NeoMetadata:
    # since this smart contract will call another, it needs to have permission to do so on the manifest
    meta = NeoMetadata()
    meta.add_permission(contract='*', methods='*')
    return meta
