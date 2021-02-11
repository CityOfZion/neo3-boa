from boa3.builtin import public
from boa3.builtin.interop.runtime import executing_script_hash
from boa3.builtin.type import UInt160


@public
def Main(example: UInt160) -> UInt160:
    global executing_script_hash
    executing_script_hash = example
    return executing_script_hash
