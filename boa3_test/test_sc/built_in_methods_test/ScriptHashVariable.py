from boa3.builtin.compile_time import public
from boa3.builtin.contract import to_script_hash


@public
def Main(a: bytes) -> bytes:
    return to_script_hash(a)
