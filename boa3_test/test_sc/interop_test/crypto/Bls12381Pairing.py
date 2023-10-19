from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.interop.crypto import bls12_381_pairing, IBls12381


@public
def main(g1: IBls12381, g2: IBls12381) -> IBls12381:
    return bls12_381_pairing(g1, g2)
