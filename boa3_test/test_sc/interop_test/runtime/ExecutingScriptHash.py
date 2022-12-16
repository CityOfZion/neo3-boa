from boa3.builtin.compile_time import public
from boa3.builtin.interop.runtime import executing_script_hash
from boa3.builtin.type import UInt160


@public
def Main() -> UInt160:
    return executing_script_hash
