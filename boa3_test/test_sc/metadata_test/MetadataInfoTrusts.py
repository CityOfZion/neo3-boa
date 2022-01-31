from boa3.builtin import NeoMetadata, metadata


def Main() -> int:
    return 5


@metadata
def author_manifest() -> NeoMetadata:
    meta = NeoMetadata()

    # values added to manifest
    meta.add_trusted_source("0x1234567890123456789012345678901234567890")
    meta.add_trusted_source("0x1234567890123456789012345678901234abcdef")
    meta.add_trusted_source("030000123456789012345678901234567890123456789012345678901234abcdef")
    meta.add_trusted_source("020000123456789012345678901234567890123456789012345678901234abcdef")

    # values not added to manifest
    meta.add_trusted_source("0x123456789012345678901234567890123abcdefg")   # only hex values are valid
    meta.add_trusted_source("0x1234567890123456789012345678901234567890")   # can't repeat values
    meta.add_trusted_source("030000123456789012345678901234567890123456789012345678901234abcdef")   # can't repeat values
    meta.add_trusted_source("03000012345678901234567890123456789012345678901234567890123abcdefg")   # only hex values are valid
    meta.add_trusted_source("000000123456789012345678901234567890123456789012345678901234567890")   # public keys must begin with 03 or 02

    return meta
