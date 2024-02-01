from boa3.builtin.compile_time import NeoMetadata


def Main() -> int:
    meta = example()
    return 5


def example() -> NeoMetadata:
    # this function won't exist in the scope of the smart contract, so it can't be called by other functions
    meta = NeoMetadata()
    meta.description = ''
    return meta
