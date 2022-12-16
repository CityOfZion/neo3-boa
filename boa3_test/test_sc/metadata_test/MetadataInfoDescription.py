from boa3.builtin.compile_time import NeoMetadata, metadata, public


@public
def Main() -> int:
    return 5


@metadata
def description_manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.description = 'This is an example'
    return meta
