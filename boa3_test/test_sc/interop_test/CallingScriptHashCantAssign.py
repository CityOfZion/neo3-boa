from boa3.builtin.interop.runtime import calling_script_hash
from boa3.builtin.type import UInt160


def Main(example: UInt160) -> UInt160:
    global calling_script_hash
    calling_script_hash = example
    return calling_script_hash
