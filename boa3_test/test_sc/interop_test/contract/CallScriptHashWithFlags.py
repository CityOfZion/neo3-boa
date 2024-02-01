from typing import Any

from boa3.builtin.compile_time import NeoMetadata, public
from boa3.builtin.interop.contract import CallFlags, call_contract
from boa3.builtin.type import UInt160


@public
def Main(scripthash: UInt160, method: str, args: list, flags: CallFlags) -> Any:
    return call_contract(scripthash, method, args, flags)


def manifest_metadata() -> NeoMetadata:
    # since this smart contract will call another, it needs to have permission to do so on the manifest
    meta = NeoMetadata()
    meta.add_permission(contract='*', methods='*')
    return meta
