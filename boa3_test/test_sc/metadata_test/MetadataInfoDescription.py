from boa3.builtin.compile_time import NeoMetadata, public


@public
def Main() -> int:
    return 5


def description_manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.description = 'This is an example'
    return meta
