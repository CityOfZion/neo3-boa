from boa3.sc.compiletime import NeoMetadata, public


@public
def Main() -> int:
    return 5


def author_manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.author = 'Test'
    return meta
