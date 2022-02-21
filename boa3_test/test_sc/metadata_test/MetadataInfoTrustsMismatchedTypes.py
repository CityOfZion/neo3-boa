from boa3.builtin import NeoMetadata, metadata


def Main() -> int:
    return 5


@metadata
def trusts_manifest() -> NeoMetadata:
    meta = NeoMetadata()

    meta.add_trusted_source(0x0123456789012345678901234567890123456789)
    meta.add_trusted_source(b'0123456789012345678901234567890123456789')
    meta.add_trusted_source(True)
    return meta
