from boa3.builtin import NeoMetadata, metadata, public


@public
def Main() -> int:
    return 5


@metadata
def email_manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.source = 'https://github.com/CityOfZion/neo3-boa'
    return meta
