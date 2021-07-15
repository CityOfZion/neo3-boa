from boa3.builtin import NeoMetadata, metadata


def Main() -> int:
    return 5


@metadata
def standards_manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.supported_standards = 'NEP-11'
    return meta
