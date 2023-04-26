from boa3.builtin.compile_time import NeoMetadata, metadata, public
from boa3.builtin.nativecontract.neo import NEO


@public
def main() -> int:
    return NEO.totalSupply()


@metadata
def permissions_manifest() -> NeoMetadata:
    meta = NeoMetadata()

    meta.add_permission(contract='*', methods='*')

    return meta
