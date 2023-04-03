from boa3.builtin.compile_time import public
from boa3.builtin.interop.crypto import bls12_381_deserialize


@public
def main() -> bytes:
    return bls12_381_deserialize(b'1')
