from boa3.builtin.compile_time import public
from boa3.builtin.contract import to_script_hash
from boa3.builtin.type import ECPoint


@public
def Main(public_key: ECPoint) -> bytes:
    return to_script_hash(public_key)
