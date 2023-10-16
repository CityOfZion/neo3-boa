from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.interop.crypto import bls12_381_equal


@public
def main(g1: Any, g2: Any) -> bool:
    return bls12_381_equal(g1, g2)
