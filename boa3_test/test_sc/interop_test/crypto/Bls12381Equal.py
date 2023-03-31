from boa3.builtin.compile_time import public
from boa3.builtin.interop.crypto import bls12_381_equal


@public
def main() -> bool:
    return bls12_381_equal(b'1', b'2')
