from boa3.builtin import public, to_script_hash
from boa3.builtin.type import ECPoint


@public
def Main(public_key: ECPoint) -> bytes:
    return to_script_hash(public_key)
