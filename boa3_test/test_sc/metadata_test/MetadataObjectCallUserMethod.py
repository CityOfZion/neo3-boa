from boa3.builtin.compile_time import NeoMetadata


def Main() -> int:
    meta = NeoMetadata()  # this object can be only used inside metadata function
    return 5
