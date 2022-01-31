from boa3.builtin import NeoMetadata, metadata


def Main() -> int:
    return 5


@metadata
def author_manifest() -> NeoMetadata:
    meta = NeoMetadata()

    # the * wildcard will remove all but itself from trusts
    meta.add_trusted_source("0x1234567890123456789012345678901234567890")
    meta.add_trusted_source("*")
    meta.add_trusted_source("0x1234567890123456789012345678901234567890")

    return meta
