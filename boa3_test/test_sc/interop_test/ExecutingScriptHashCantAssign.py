from boa3.builtin import public
from boa3.builtin.interop.runtime import executing_script_hash


@public
def Main(example: bytes) -> bytes:
    global executing_script_hash
    executing_script_hash = example
    return executing_script_hash
