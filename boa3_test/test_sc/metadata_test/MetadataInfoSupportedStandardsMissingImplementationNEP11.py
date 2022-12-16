from boa3.builtin.compile_time import NeoMetadata, metadata


def Main() -> int:
    return 5


@metadata
def standards_manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.supported_standards = ['NEP-11']  # for nep11, boa checks if the standard is implemented
    return meta
