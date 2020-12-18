from boa3.builtin.interop.contract import NEO
from boa3.builtin.type import UInt160


def Main(example: UInt160) -> UInt160:
    global NEO
    NEO = example
    return NEO
