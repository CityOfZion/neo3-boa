from boa3.builtin.compile_time import NeoMetadata, metadata, public


@public
def Main() -> int:
    return 5


@metadata
def manifest() -> NeoMetadata:
    from boa3.builtin.compile_time import NeoMetadata
    return NeoMetadata()
