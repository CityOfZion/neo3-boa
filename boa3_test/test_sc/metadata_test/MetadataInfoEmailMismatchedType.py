from boa3.builtin.compile_time import NeoMetadata, metadata


def Main() -> int:
    return 5


@metadata
def email_manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.email = False
    return meta
