from typing import cast

from boa3.sc.compiletime import NeoMetadata, public
from boa3.sc.types import UInt160
from boa3.sc.utils import call_contract


@public
def Main(scripthash: bytes, method: str, args: list) -> bool:
    call_contract(cast(UInt160, scripthash), method, args)
    return True


def manifest_metadata() -> NeoMetadata:
    # since this smart contract will call another, it needs to have permission to do so on the manifest
    meta = NeoMetadata()
    meta.add_permission(contract='*', methods='*')
    return meta
