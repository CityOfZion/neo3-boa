from boa3.sc.compiletime import NeoMetadata


def Main() -> int:
    return 5


def description_manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.description = [0, 4, 8, 12]
    return meta
