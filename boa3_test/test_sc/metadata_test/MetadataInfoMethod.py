from boa3.sc.compiletime import NeoMetadata, public


@public
def Main() -> int:
    return 5


def manifest() -> NeoMetadata:
    from boa3.sc.compiletime import NeoMetadata
    return NeoMetadata()
