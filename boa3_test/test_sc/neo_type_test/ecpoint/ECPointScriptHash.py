from boa3.builtin.compile_time import public
from boa3.builtin.type import ECPoint


@public
def Main(public_key: ECPoint) -> bytes:
    return public_key.to_script_hash()
