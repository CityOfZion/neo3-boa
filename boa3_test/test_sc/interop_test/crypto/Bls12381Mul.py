from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.interop.crypto import bls12_381_mul, IBls12381


@public
def main(g: IBls12381, mul: bytes) -> IBls12381:
    return bls12_381_mul(g, mul, True)
