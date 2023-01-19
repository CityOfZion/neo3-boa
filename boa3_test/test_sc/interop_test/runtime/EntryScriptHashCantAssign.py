from boa3.builtin.compile_time import public
from boa3.builtin.interop.runtime import entry_script_hash
from boa3.builtin.type import UInt160


@public
def main(example: UInt160) -> UInt160:
    entry_script_hash = example
    return entry_script_hash


def interop_call():
    x = entry_script_hash
