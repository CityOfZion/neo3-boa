from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.interop.crypto import bls12_381_deserialize


@public
def main(data: bytes) -> Any:
    return bls12_381_deserialize(data)
