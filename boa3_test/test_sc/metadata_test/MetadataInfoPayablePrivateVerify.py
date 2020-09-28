from boa3.builtin import NeoMetadata, metadata


def Main() -> int:
    return 5


def verify() -> bool:
    return False


@metadata
def payable_manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.is_payable = True
    return meta
