from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.interop.crypto import bls12_381_serialize


@public
def main(g: Any) -> bytes:
    return bls12_381_serialize(g)
