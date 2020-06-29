from boa3.builtin import metadata, NeoMetadata


def Main() -> int:
    return 5


@metadata
def manifest() -> NeoMetadata:
    from boa3.builtin import NeoMetadata
    return NeoMetadata()
