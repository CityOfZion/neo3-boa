from boa3.builtin.compile_time import NeoMetadata


def Main() -> int:
    return 5


def author_manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.author = 98
    return meta
