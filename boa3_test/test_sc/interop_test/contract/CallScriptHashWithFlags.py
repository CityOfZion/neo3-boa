from typing import Any

from boa3.sc.compiletime import NeoMetadata, public
from boa3.sc.types import UInt160, CallFlags
from boa3.sc.utils import call_contract


@public
def Main(scripthash: UInt160, method: str, args: list, flags: CallFlags) -> Any:
    return call_contract(scripthash, method, args, flags)


def manifest_metadata() -> NeoMetadata:
    # since this smart contract will call another, it needs to have permission to do so on the manifest
    meta = NeoMetadata()
    meta.add_permission(contract='*', methods='*')
    return meta
