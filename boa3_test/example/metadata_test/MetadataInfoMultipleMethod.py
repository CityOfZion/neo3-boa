from boa3.builtin import metadata, NeoMetadata


def Main() -> int:
    return 5


@metadata
def manifest_func1() -> NeoMetadata:
    from boa3.builtin import NeoMetadata
    return NeoMetadata()


@metadata  # this decorator can be applied to one function only
def manifest_func2() -> NeoMetadata:
    from boa3.builtin import NeoMetadata
    return NeoMetadata()
