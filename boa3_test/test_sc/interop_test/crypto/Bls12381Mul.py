from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.interop.crypto import bls12_381_mul


@public
def main(g: Any, mul: bytes) -> Any:
    return bls12_381_mul(g, mul, True)
