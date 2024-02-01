from boa3.builtin.compile_time import NeoMetadata, public


@public
def Main() -> int:
    return 5


def manifest() -> NeoMetadata:
    from boa3.builtin.compile_time import NeoMetadata
    return NeoMetadata()
