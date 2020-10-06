from boa3.builtin.interop.contract import NEO


def Main(example: bytes) -> bytes:
    global NEO
    NEO = example
    return NEO
