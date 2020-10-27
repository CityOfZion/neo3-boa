from boa3.builtin import NeoMetadata, metadata


def Main() -> int:
    return 5


@metadata
def extras_manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.author = 'Test'
    meta.email = 'test@test.com'
    meta.description = 'This is an example'
    return meta
