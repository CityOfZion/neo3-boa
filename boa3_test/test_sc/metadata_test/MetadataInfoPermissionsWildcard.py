from boa3.builtin.compile_time import NeoMetadata, metadata, public


@public
def Main() -> int:
    return 5


@metadata
def permissions_manifest() -> NeoMetadata:
    meta = NeoMetadata()

    meta.add_permission(contract='*', methods='*')

    return meta
