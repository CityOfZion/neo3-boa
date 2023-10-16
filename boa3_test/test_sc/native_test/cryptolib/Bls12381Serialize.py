from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.cryptolib import CryptoLib


@public
def main(g: Any) -> bytes:
    return CryptoLib.bls12_381_serialize(g)
