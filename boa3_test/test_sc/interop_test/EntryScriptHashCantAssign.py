from boa3.builtin.interop.runtime import entry_script_hash
from boa3.builtin.type import UInt160


def main(example: UInt160) -> UInt160:
    global entry_script_hash
    entry_script_hash = example
    return entry_script_hash
