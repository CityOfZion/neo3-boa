from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.interop.crypto import bls12_381_deserialize, IBls12381


@public
def main(data: bytes) -> IBls12381:
    return bls12_381_deserialize(data)
