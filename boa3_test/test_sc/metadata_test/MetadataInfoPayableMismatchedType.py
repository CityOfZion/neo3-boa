from boa3.builtin import NeoMetadata, metadata


def Main() -> int:
    return 5


@metadata
def payable_manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.is_payable = 1
    return meta
