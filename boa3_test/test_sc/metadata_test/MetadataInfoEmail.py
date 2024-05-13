from boa3.sc.compiletime import NeoMetadata, public


@public
def Main() -> int:
    return 5


def email_manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.email = 'test@test.com'
    return meta
