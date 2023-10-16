from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.cryptolib import CryptoLib


@public
def main(g: Any, mul: bytes) -> Any:
    return CryptoLib.bls12_381_mul(g, mul, True)
