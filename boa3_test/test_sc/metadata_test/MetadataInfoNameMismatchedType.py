from boa3.builtin.compile_time import NeoMetadata


def Main() -> int:
    return 5


def name_manifest() -> NeoMetadata:
    meta = NeoMetadata()

    meta.name = 1234567

    return meta
