from boa3.builtin.compile_time import NeoMetadata, metadata, public


@public
def Main() -> int:
    return 5


@metadata
def manifest_func1() -> NeoMetadata:
    from boa3.builtin.compile_time import NeoMetadata
    meta = NeoMetadata()
    meta.description = 'func1'
    return meta


@metadata  # this decorator can be applied to one function only
def manifest_func2() -> NeoMetadata:
    from boa3.builtin.compile_time import NeoMetadata
    meta = NeoMetadata()
    meta.description = 'func2'
    return meta
