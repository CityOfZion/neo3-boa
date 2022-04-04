from boa3.builtin import NeoMetadata, metadata, public


@public
def Main() -> int:
    return 5


@metadata
def standards_manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.supported_standards = ['NEP-5']
    return meta
