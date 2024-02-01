from boa3.builtin.compile_time import NeoMetadata, public


@public
def Main() -> int:
    return 5


def trusts_manifest() -> NeoMetadata:
    meta = NeoMetadata()

    # values added to manifest
    meta.add_trusted_source("0x1234567890123456789012345678901234567890")
    meta.add_trusted_source("0x1234567890123456789012345678901234abcdef")
    meta.add_trusted_source("035a928f201639204e06b4368b1a93365462a8ebbff0b8818151b74faab3a2b61a")
    meta.add_trusted_source("03cdb067d930fd5adaa6c68545016044aaddec64ba39e548250eaea551172e535c")

    # values not added to manifest
    meta.add_trusted_source("0x123456789012345678901234567890123abcdefg")   # only hex values are valid
    meta.add_trusted_source("0x1234567890123456789012345678901234567890")   # can't repeat values
    meta.add_trusted_source("03cdb067d930fd5adaa6c68545016044aaddec64ba39e548250eaea551172e535c")   # can't repeat values
    meta.add_trusted_source("03000012345678901234567890123456789012345678901234567890123abcdefg")   # only hex values are valid
    meta.add_trusted_source("000000123456789012345678901234567890123456789012345678901234567890")   # public keys must begin with 03 or 02

    return meta
