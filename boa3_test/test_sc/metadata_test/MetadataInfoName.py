from boa3.builtin.compile_time import NeoMetadata, metadata, public


@public
def Main() -> int:
    return 5


@metadata
def name_manifest() -> NeoMetadata:
    meta = NeoMetadata()

    meta.name = "SmartContractCustomName"

    return meta
