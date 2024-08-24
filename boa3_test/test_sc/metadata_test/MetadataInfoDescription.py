from boa3.sc.compiletime import NeoMetadata, public


@public
def Main() -> int:
    return 5


def description_manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.description = 'This is an example'
    return meta
