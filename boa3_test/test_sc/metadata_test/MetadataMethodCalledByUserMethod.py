from boa3.builtin import NeoMetadata, metadata


def Main() -> int:
    meta = example()
    return 5


@metadata
def example() -> NeoMetadata:
    # this function won't exist in the scope of the smart contract, so it can't be called by other functions
    meta = NeoMetadata()
    meta.description = ''
    return meta
