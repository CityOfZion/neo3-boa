from boa3.builtin import NeoMetadata, metadata, public


@public
def main() -> int:
    return 5


@metadata
def permissions_manifest() -> NeoMetadata:
    meta = NeoMetadata()

    return meta
