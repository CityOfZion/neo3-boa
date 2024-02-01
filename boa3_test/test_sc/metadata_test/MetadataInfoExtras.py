from boa3.builtin.compile_time import NeoMetadata, public


@public
def Main() -> int:
    return 5


def extras_manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.author = 'Test'
    meta.email = 'test@test.com'
    meta.description = 'This is an example'
    return meta
