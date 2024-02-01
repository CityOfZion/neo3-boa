from boa3.builtin.compile_time import NeoMetadata, public


@public
def Main() -> int:
    return 5


def manifest_func1() -> NeoMetadata:
    from boa3.builtin.compile_time import NeoMetadata
    meta = NeoMetadata()
    meta.description = 'func1'
    return meta


# this function will be ignored by the compiler
def manifest_func2() -> NeoMetadata:
    from boa3.builtin.compile_time import NeoMetadata
    meta = NeoMetadata()
    meta.description = 'func2'
    return meta
