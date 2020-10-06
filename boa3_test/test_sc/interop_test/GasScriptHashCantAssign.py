from boa3.builtin.interop.contract import GAS


def Main(example: bytes) -> bytes:
    global GAS
    GAS = example
    return GAS
