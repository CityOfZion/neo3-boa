from boa3.builtin import NeoMetadata, metadata


def Main() -> int:
    return 5


@metadata
def permissions_manifest() -> NeoMetadata:
    meta = NeoMetadata()
    return meta
