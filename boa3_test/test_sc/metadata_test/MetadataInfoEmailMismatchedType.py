from boa3.sc.compiletime import NeoMetadata


def Main() -> int:
    return 5


def email_manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.email = False
    return meta
