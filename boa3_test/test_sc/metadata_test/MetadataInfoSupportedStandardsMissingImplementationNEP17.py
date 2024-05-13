from boa3.sc.compiletime import NeoMetadata


def Main() -> int:
    return 5


def standards_manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.supported_standards = ['NEP-17']  # for nep17, boa checks if the standard is implemented
    return meta
