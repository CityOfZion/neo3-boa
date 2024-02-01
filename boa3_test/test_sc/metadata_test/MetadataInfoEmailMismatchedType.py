from boa3.builtin.compile_time import NeoMetadata


def Main() -> int:
    return 5


def email_manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.email = False
    return meta
