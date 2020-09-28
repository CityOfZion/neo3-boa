from boa3.builtin import NeoMetadata, metadata


def Main() -> int:
    return 5


@metadata
def author_manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.author = 98
    return meta
