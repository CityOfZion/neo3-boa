from boa3.builtin import NeoMetadata, metadata, public


@public
def Main() -> int:
    return 5


@metadata
def name_manifest() -> NeoMetadata:
    meta = NeoMetadata()

    return meta