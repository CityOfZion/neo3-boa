from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.interop.crypto import bls12_381_serialize, IBls12381


@public
def main(g: IBls12381) -> bytes:
    return bls12_381_serialize(g)
