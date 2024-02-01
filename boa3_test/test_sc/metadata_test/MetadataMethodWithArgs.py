from boa3.builtin.compile_time import NeoMetadata


def Main() -> int:
    return 5


def example(arg0: int, arg1: str) -> NeoMetadata:
    # this function doesn't allow arguments
    return NeoMetadata()
