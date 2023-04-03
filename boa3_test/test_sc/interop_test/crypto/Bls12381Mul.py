from boa3.builtin.compile_time import public
from boa3.builtin.interop.crypto import bls12_381_mul


@public
def main() -> bytes:
    return bls12_381_mul(b'1', 2, True)
