from boa3.builtin import NeoMetadata, metadata


def Main() -> int:
    return 5


@metadata
def storage_manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.has_storage = True
    return meta
